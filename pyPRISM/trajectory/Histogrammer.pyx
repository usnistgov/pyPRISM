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



cdef class Histogrammer:
    r'''Parallelized Histogrammer class to calculate :math:`g_{\alpha,\beta}(r)`

    .. warning::

        This pyPRISM functionality is still under testing. Use with caution.

    **Mathematical Definition**

    .. math::
            
        TBA


    **Variable Definitions**

        TBA


    **Description**


    TBA

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

        # create Histogrammer object
        debyer = pyPRISM.trajectory.Histogrammer(domain=domain,nthreads=4)

        # calculate gr_1_1 
        mask1 = (types == 1)
        positions1 =  positions[:,mask1,:]
        molecules1 =  molecules[mask1]
        mask2 = (types == 1)
        positions2 =  positions[:,mask2,:]
        molecules2 =  molecules[mask2]
        selfHist = True
        gr_1_1  = debyer.calculate(positions1, positions2, molecules1, molecules2, box, selfHist)

        # calculate gr_1_2
        mask1 = (types == 1)
        positions1 =  positions[:,mask1,:]
        molecules1 =  molecules[mask1]
        mask2 = (types == 2)
        positions2 =  positions[:,mask2,:]
        molecules2 =  molecules[mask2]
        selfHist = False
        gr_1_2  = debyer.calculate(positions1, positions2, molecules1, molecules2, box, selfHist)



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
                Domain object defining the points to calculate :math:`g(r)` at.

        nthreads: int
                Number of threads to use in parallel execution
        '''
        self.dr         = domain.dr
        self.dk         = domain.dk
        self.rmax       = domain.length*domain.dr
        self.rmaxsq     = self.rmax*self.rmax
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

    def calculate(self, positions1, positions2, molecules1, molecules2, box, intraHist,interHist):
        r'''Calculate g(r) from two site type trajectories

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

        intraHist,interHist: bool
            Boolean parameters to control whether intra and inter-molecular
            pairs are included.
            

        Returns
        -------
        hist: np.ndarray
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
        cdef cFloatType[:,:] thread_hist = np.zeros((self.num_chunks,self.num_bins), dtype=floatType)

        cdef cFloatType[:] Base1D         = np.zeros(self.num_bins, dtype=floatType)
        cdef cFloatType[:] hist          = np.zeros(self.num_bins, dtype=floatType)
        cdef cFloatType[:] frame_hist    = np.zeros(self.num_bins, dtype=floatType)

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
            frame_hist[:]    = Base1D
            thread_hist[:,:] = Base2D

            self._calculate(R1_frame,R2_frame,M1,M2,nbeads1,nbeads2,box_frame,frame_hist,thread_hist,chunks,intraHist,interHist)

            for k in range(self.num_bins):
                hist[k] += frame_hist[k]


        # divide by the number of frames
        for k in range(self.num_bins):
            hist[k] = hist[k]/count

        return np.array(hist)

    cdef void _calculate(self,
                             cFloatType[:,:] R1, 
                             cFloatType[:,:] R2, 
                             cIntType[:] M1,
                             cIntType[:] M2,
                             cIntType nbeads1,
                             cIntType nbeads2,
                             cFloatType[:] L,
                             cFloatType[:] hist,
                             cFloatType[:,:] thread_hist,
                             cIntType[:,:] chunks,
                             bint intraHist,
                             bint interHist) nogil:
        r'''hist calculation driver

        The main optimization is that it is parallelized using OpenMP such that
        the calculation is split up across several memory-sharing threads.
        Each thread takes a chunk of the positions in the first array and
        calculates the spatial histogram between all of the positions in the
        second array.  See :func:`pyPRISM.trajectory.Histogrammer.Histogrammer._chunks` for
        how the chunking
        occurs.

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

        hist: np.ndarray
            array which will be filled with final calculated
            :math:`g(r)` values

        thread_hist: np.ndarray
            Stack of hist arrays for each thread. The first dimension length
            is equal to the number of threads.

        chunks: np.ndarray
            See :func:`pyPRISM.trajectory.Debyer.Debyer._chunks`

        selfHist: bool
            Set to *True* if :math:`\alpha == \beta` and False otherwise.

        '''
        cdef cFloatType num_pairs
        cdef cFloatType lx  = L[0]
        cdef cFloatType lx2 = L[0]/2.0
        cdef cFloatType ly  = L[1]
        cdef cFloatType ly2 = L[1]/2.0
        cdef cFloatType lz  = L[2]
        cdef cFloatType lz2 = L[2]/2.0
        cdef cFloatType dx,dy,dz,rsq

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
            i1 = chunks[thread_num,1]

            for i in range(i0,i1):
                for j in range(nbeads2):

                    # intra-molecular check
                    if ((not intraHist) and (M1[i]==M2[j])):
                        continue
                    elif ((not interHist) and (M1[i]!=M2[j])):
                        continue
                    elif ((M1[i]==M2[j]) and (i==j)):
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
        
                    rsq = dx*dx + dy*dy + dz*dz
                    if rsq<self.rmaxsq:
                      q = (int) (c_sqrt(rsq)/self.dr)
                      thread_hist[thread_num,q] = thread_hist[thread_num,q] + 1
            
            
        for thread_num in range(self.num_chunks):
          for q in range(self.num_bins):
            hist[q] += thread_hist[thread_num,q]

        



