#!python
#cython: boundscheck=False
#cython: cdivision=True
#cython: nonecheck=False
#cython: embedsignature=True

import multiprocessing
from math import ceil

import numpy as np
import warnings
cimport numpy as np
cimport cython


# Fast c-functions
from cython.parallel cimport prange,parallel,threadid
from libc.math cimport fabs as c_fabs
from libc.math cimport sqrt as c_sqrt
from libc.math cimport sin as c_sin
from libc.stdio cimport printf

# Define numerical types
intType    = np.int
floatType  = np.float32
ctypedef np.int_t     cIntType
ctypedef np.float32_t cFloatType



cdef class Debyer:
    r'''Parallelized Debye method to calculate :math:`\hat{\omega}_{\alpha,\beta}(k)`

    .. warning::

        This pyPRISM functionality is still under testing. Use with caution.

    **Mathematical Definition**

    .. math::

        \hat{\omega}_{\alpha,\beta}(k) = \delta_{\alpha,\beta} +
        \frac{C_{\alpha,\beta}}{N_{frame}} \sum_f \sum_{i,j}
        \frac{\sin(kr^{f}_{ij})}{kr^{f}_{ij}}

    **Variable Definitions**

        - :math:`\hat{\omega}_{\alpha,\beta}(k)` 
            Intra-molecular correlation function in Fourier-space

        - :math:`\delta_{\alpha,\beta}` 
            Kronecker delta for when considering a self (:math:`\alpha == \beta`)
            versus not-self (:math:`\alpha /= \beta`) site type pair.

        - :math:`N_{frame}`
            Number of frames in simulation trajectory

        - :math:`C_{\alpha,\beta}`
            Scaling coefficient. If :math:`\alpha == \beta`, then
            :math:`C_{\alpha,\beta} = 1/N_{\alpha}` else
            :math:`C_{\alpha,\beta} = 1/(N_{\alpha} + N_{\beta})`
            
    
        - :math:`r^{f}_{i,j}`
            At frame :math:`f` of simulation, the scalar distance between sites
            with index i and j. 

        - :math:`k`
            Wavenumber of calculation.

    **Description**

    One of the most powerful uses of PRISM is to combine it with modern
    simulation techniques to calculate the intra-molecular correlation
    functions :math:`\hat{\omega}(k)`. This allows PRISM to be used for systems
    which do not have analytical descriptions for their :math:`\hat{\omega}(k)`
    and, furthermore, allows PRISM to predic the structure of non-ideal
    systems.

    Unfortunately, this calculation is extremely computationally intensive and
    requires care to calculate correctly. Here we provide a parallelized
    implementation of the Debye Method which can be used to calculate
    :math:`\hat{\omega}(k)` for small to medium sized simulations. 
    
    This method works by allowing the user to selectively provide two sets of
    coordinate trajectories. To calculate :math:`\hat{\omega}(k)` between
    site-types :math:`\alpha` and :math:`\beta`, the user should pass one
    trajectory of all sites of type :math:`\alpha` and the other where all
    sites are of type :math:`\beta`. To calculate a self
    :math:`\hat{\omega}(k)` where :math:`\alpha == \beta` (selfOmega=*True*),
    both trajectories should be the same. Note that selfOmega should be
    correctly set in either case. 

    The calculate method below takes six arguments: positions1, positions2,
    molecules1, molecules2, box, selfOmega. 
    
    The positions1 and positions2 arguments are numpy array containing multiple
    frames of coordinates. Each of the two arrays should only contain the
    coordinates of the site-type pair being considered. In other words,
    positions1 should have a trajectory of positions for site type
    :math:`\alpha` and positions2 for :math:`\beta` when calculating
    :math:`\hat{\omega}_{\alpha,\beta}(k)`. If :math:`\alpha == \beta`, the
    positions1 and positions2 should be the same array.  

    The molecules1 and molecules2 arguments specify to which molecule each site
    belongs.  These arrays are necessary for calculations using trajectories
    that contain multiple molecules. For each site in the simulation of a
    site-type, these lists have an integer index which specify which molecule
    the site belongs to. All sites which share the same molecular index in this
    array belong to the same molecue. For single molecule simulations, an array
    of zeros or ones can be specified. 

    See the example below for an example of this classes use.

    .. note::

        Note that the num_chunks argument **does not** set the number of
        threads used in the calculation. This is governed by the
        OMP_NUM_THREADS (at least on \*nix and OSX). If you have many cores on
        your machine, you may actually see improved performance if you reduce
        the value of OMP_NUM_THREADS from its maximum. Setting this variable
        is also useful if you're sharing a machine or node. If running a
        script, you can set this variables globally:

        .. code-block:: bash

            $ export OMP_NUM_THREADS=4

        or locally for a single execution

        .. code-block:: bash

            $ OMP_NUM_THREADS=4 python pyPRISM_script.py

    .. note::

        As currently written, this class assumes periodicity in all dimensions. 

    Example
    -------
    Below we consider an arbitrary system  that has at least two types of sites in it.

    .. code-block:: python

        import pyPRISM
        import numpy as np

        
        # load position, type, and molecule information using a users method of
        # choice. For the array sizes, F = number of frames from simulation, N =
        # total number of atoms/beads/sites
        positions = ...  # 3D Array of size (F,N,3)
        types = ...      # 1D Array of size (N)
        molecules = ...  # 1D Array of size (N)
        box = ...        # 2D Array of size (F,3)

        # create pyPRISM domain
        domain = pyPRISM.Domain(dr = 0.25, length = 1024)

        # create Debyer object
        debyer = pyPRISM.trajectory.Debyer(domain=domain,nthreads=4)

        # calculate omega_1_1 
        mask1 = (types == 1)
        positions1 =  positions[:,mask1,:]
        molecules1 =  molecules[mask1]
        mask2 = (types == 1)
        positions2 =  positions[:,mask2,:]
        molecules2 =  molecules[mask2]
        selfOmega = True
        omega_1_1  = debyer.calculate(positions1, positions2, molecules1, molecules2, box, selfOmega)

        # calculate omega_1_2
        mask1 = (types == 1)
        positions1 =  positions[:,mask1,:]
        molecules1 =  molecules[mask1]
        mask2 = (types == 2)
        positions2 =  positions[:,mask2,:]
        molecules2 =  molecules[mask2]
        selfOmega = False
        omega_1_2  = debyer.calculate(positions1, positions2, molecules1, molecules2, box, selfOmega)



    '''
    cdef cFloatType dr
    cdef cFloatType dk
    cdef cFloatType rmax
    cdef cFloatType rmaxsq
    cdef cIntType num_chunks
    cdef cIntType num_bins

    def __init__(self, domain, nthreads=None):
        '''Constructor

        Arguments
        ---------
        domain: pyPRISM.Domain
                Domain object defining the points to calculate :math:`\omega` at.

        nthreads: int
                Number of threads to use in parallel execution
        '''
        self.dr         = domain.dr
        self.dk         = domain.dk
        self.rmax       = domain.length*domain.dr
        self.rmaxsq = self.rmax*self.rmax
        self.num_chunks = nthreads if nthreads is not None else multiprocessing.cpu_count()
        self.num_bins = int(domain.length)

        # warnings.warn('This pyPRISM functionality is still under testing. Use with caution.')
    def _chunk(self,int num_indices, int num_chunks):
        ''' Divide consecutive indices into chunks

        This method evenly divides indices in the range
        :math:`[0,num_indices-1]` into a specified number of chunks. This
        method is used to divide the parallelized calculation across a number
        of threads. In particular, this function handles the case where the
        number of indicies does not divide evenly into the number of chunks. In
        this case, the indicies are dividied evenly save the final chunk which
        is made smaller to accomodate the remainder of the indices. 

        .. warning::

            Due to the nature of this calculation, the Cython wraparound
            optimization cannot be enabled for this class.

        Arguments
        ---------
        num_indices: int
            Number of indices to split up. 

        num_chunks:  int
            Number of chunks to divide indices over

        Returns
        -------
        chunked_indices: np.ndarray, type int, size (num_chunks,2)
            2-D Number array where the first dimension corresponds to the chunk
            index. In a given row, the first column has the starting index of a
            given chunk and the second has the end index of that chunk. Note
            that the second column is shifted by 1 so that the end index will
            work correctly with range().
        '''
        cdef cIntType[:,:] chunked_indices = np.zeros((num_chunks,2),dtype=intType)
        index_list = range(num_indices)
        len_index_list = len(index_list)
        chunk_size = int(ceil(len_index_list/float(num_chunks)))
        full_list = [index_list[i:i+chunk_size] for i in range(0,len_index_list,chunk_size)]
        for i,chunk in enumerate(full_list):
            chunked_indices[i,0] = chunk[0]
            chunked_indices[i,1] = chunk[-1]+1
        return np.array(chunked_indices)

    def calculate(self, positions1, positions2, molecules1, molecules2, box, selfOmega):
        r'''Calculate omega from two site type trajectories

        .. warning::

            The first five arguments of this method (positions1, positions2,
            molecules1, molecules2, box) **must** be numpy arrays (not Python
            lists) for this method to work.


        Arguments
        ---------

        positions1: np.ndarray, float, size (:math:`F,N_{\alpha}`,3)
            3-D numpy array containing coordinate trajectory from a simulation
            for site type :math:`\alpha`. See above for description.

        positions2: np.ndarray, float, size (:math:`F,N_{\beta}`,3)
            3-D numpy array containing coordinate trajectory from a simulation
            for site type :math:`\beta`. See above for description.
            
        molecules1: np.ndarray, float, size (:math:`N_{\alpha}`)
            1-D numpy arrays which specify the molecular identity of a site for
            sites of type :math:`\alpha`. See above for a description.

        molecules2: np.ndarray, float, size (:math:`N_{\beta}`)
            1-D numpy arrays which specify the molecular identity of a site for
            sites of type :math:`\beta`. See above for a description.

        box: np.ndarray, float, size(3)
            1-D array of box dimensions, :math:`l_{x}, l_{y}, l_{z}`

        selfOmega: bool
            Set to *True* if :math:`\alpha == \beta` and False otherwise.
            

        Returns
        -------
        omega: np.ndarray
            Intra-molecular correlation function 
            
        '''

        cdef cIntType frame,k

        cdef cFloatType[:,:,:] R1_all = positions1.astype(floatType)
        cdef cFloatType[:,:,:] R2_all = positions2.astype(floatType)
        cdef cFloatType[:,:] R1_frame, R2_frame

        cdef cFloatType[:,:] box_all = box.astype(floatType)
        cdef cFloatType[:] box_frame = np.zeros(3, dtype=floatType)

        cdef cIntType[:] M1 = molecules1
        cdef cIntType[:] M2 = molecules2

        cdef cIntType nbeads1 = positions1.shape[1]
        cdef cIntType nbeads2 = positions2.shape[1]

        cdef cIntType[:,:] chunks         = self._chunk(nbeads1,self.num_chunks)
        cdef cFloatType[:,:] Base2D       = np.zeros((self.num_chunks,self.num_bins), dtype=floatType)
        cdef cFloatType[:,:] thread_omega = np.zeros((self.num_chunks,self.num_bins), dtype=floatType)

        cdef cFloatType[:] Base1D         = np.zeros(self.num_bins, dtype=floatType)
        cdef cFloatType[:] omega          = np.zeros(self.num_bins, dtype=floatType)
        cdef cFloatType[:] frame_omega    = np.zeros(self.num_bins, dtype=floatType)

        cdef cIntType numFrames = R1_all.shape[0]

        cdef cIntType count = 0
        for frame in range(numFrames):
            count += 1

            # need to gather positions and box information from trajectory
            R1_frame = R1_all[frame]
            R2_frame = R2_all[frame]
            box_frame[0] = box_all[frame,0]
            box_frame[1] = box_all[frame,1]
            box_frame[2] = box_all[frame,2]

            # need to "reset" these arrays for each loop. This command copies
            # the zeros from  the Base1D and Base2D arrays into the frame_ and
            # thread_ arrays
            frame_omega[:]    = Base1D
            thread_omega[:,:] = Base2D

            self._calculate(R1_frame,R2_frame,M1,M2,nbeads1,nbeads2,box_frame,frame_omega,thread_omega,chunks,selfOmega)


            for k in range(self.num_bins):
                omega[k] += frame_omega[k]


        # divide by the number of frames
        for k in range(self.num_bins):
            omega[k] = omega[k]/count

        return np.array(omega)

    cdef void _calculate(self,
                             cFloatType[:,:] R1, 
                             cFloatType[:,:] R2, 
                             cIntType[:] M1,
                             cIntType[:] M2,
                             cIntType nbeads1,
                             cIntType nbeads2,
                             cFloatType[:] L,
                             cFloatType[:] omega,
                             cFloatType[:,:] thread_omega,
                             cIntType[:,:] chunks,
                             bint selfOmega) nogil:
        r'''omega calculation driver

        The main optimization is that it is parallelized using OpenMP such that
        the calculation is split up across several memory-sharing threads.
        Each thread takes a chunk of the positions in the first array and
        calculates the :math:`\hat{\omega}` against all of the positions in the
        second array.  See :func:`pyPRISM.trajectory.Debyer.Debyer._chunks` for
        how the chunking
        occurs.

        Beyond this, the method applies a number of optimizations to speed up
        the calculation of omega:

             - if selfOmega == *True*, the function skips double couting by
               taking advantage of the fact that :math:`r_{i,j} == r_{j,i}`.

             - if selfOmega == *True*, the function skips the calculation of i ==
               j pairs. These pairs contribute, in total, to simply shifting
               the curve vertically by 1.0


             - We apply a cutoff so to avoid part of the calculation if the
               distance is outside of the domain


        .. note::

            In order to allow this method to be parallelized, it is restricted such
            that it can only be called from a Cython-compiled function. 

        Arguments
        ---------
        R1,R2: np.ndarray
            positions arrays for a single frame

        M1,M2: np.ndarray
            molecule index arrays

        nbeads1,nbeads2: int
            number of sites for site type :math:`\alpha1` or :math:`\beta`

        L: np.ndarray
            box lengths

        omega: np.ndarray
            array which will be filled with final calculated
            :math:`\hat{omega}(k)` values

        thread_omega: np.ndarray
            Stack of omega arrays for each thread. The first dimension length
            is equal to the number of threads.

        chunks: np.ndarray
            See :func:`pyPRISM.trajectory.Debyer.Debyer._chunks`

        selfOmega: bool
            Set to *True* if :math:`\alpha == \beta` and False otherwise.

        '''
        cdef cFloatType num_pairs
        cdef cFloatType lx  = L[0]
        cdef cFloatType lx2 = L[0]/2.0
        cdef cFloatType ly  = L[1]
        cdef cFloatType ly2 = L[1]/2.0
        cdef cFloatType lz  = L[2]
        cdef cFloatType lz2 = L[2]/2.0
        cdef cFloatType dx,dy,dz,r,k

        cdef cIntType tot_natoms 
        
        # loop indices for position indices
        cdef Py_ssize_t i,j,i0,i1,j0,j1

        # loop indices for wavenumber index
        cdef Py_ssize_t q

        cdef Py_ssize_t thread_num
        cdef Py_ssize_t pair_count = 0;


        for thread_num in prange(self.num_chunks, 
                                 schedule='static',
                                 chunksize=1):

            i0 = chunks[thread_num,0]

            # If selfOmega, we don't want to double count.
            if selfOmega and (thread_num == (self.num_chunks-1)):
                i1 = chunks[thread_num,1] #- 1
            else:
                i1 = chunks[thread_num,1]

            for i in range(i0,i1):

                # If selfOmega, we don't want to double count.
                if selfOmega:
                    j0 =i+1;
                else:
                    j0 = 0

                for j in range(j0,nbeads2):

                    # intra-molecular check
                    if not (M1[i]==M2[j]):
                        continue

                    dx=c_fabs(R1[i,0] - R2[j,0])
                    dy=c_fabs(R1[i,1] - R2[j,1])
                    dz=c_fabs(R1[i,2] - R2[j,2])
        
                    # apply periodic boundary condition
                    if dx>lx2:
                        dx=dx-lx
                    if dy>ly2:
                        dy=dy-ly
                    if dz>lz2:
                        dz=dz-lz
        
                    r = c_sqrt(dx*dx + dy*dy + dz*dz)
                    for q in range(0,self.num_bins):
                        k = self.dk*(q+1);
                        thread_omega[thread_num,q] = thread_omega[thread_num,q] + c_sin(k*r)/r


        


        # sum all thread histograms into master histogram (gather)
        for thread_num in range(self.num_chunks):
            for q in range(self.num_bins):
                omega[q] = omega[q] + thread_omega[thread_num,q]

        if selfOmega:
            tot_natoms = nbeads1
        else:
            tot_natoms = nbeads1 + nbeads2

        # rescale and shift each wavenumber
        for q in range(0,self.num_bins):
            k = self.dk*(q+1);
            omega[q] = omega[q]/(k*tot_natoms)
            if selfOmega:
                omega[q] = 2.0*omega[q] + 1
