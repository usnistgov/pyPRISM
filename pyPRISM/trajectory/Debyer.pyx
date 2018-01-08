#!python
#cython: boundscheck=False
#cython: cdivision=True
#cython: nonecheck=False

import multiprocessing
from math import ceil

import numpy as np
cimport numpy as np
cimport cython

import os

from cython.parallel cimport prange,parallel,threadid
from libc.math cimport fabs as c_fabs
from libc.math cimport sqrt as c_sqrt
from libc.math cimport sin as c_sin
from libc.stdio cimport printf

intType = np.int
floatType = np.float32
doubleType = np.float
ctypedef np.int_t cIntType
ctypedef np.float32_t cFloatType
ctypedef np.float_t cDoubleType


cdef class Debyer:
    '''Parallelized Debye summation to calculate :math:`omega`

    .. warning::

        Assumes periodicity in all dimensions

    '''
    cdef float dr
    cdef float dk
    cdef float rmax
    cdef float rmaxsq
    cdef int num_threads
    cdef int num_bins
    cdef Py_ssize_t i,j,k,thread_num

    def __init__(self, domain, nthreads=None):
    '''Constructor

        Arguments
        ---------
        domain: pyPRISM.Domain
                Domain object defining the points to calculate :math:`\omega` at.

        nthreads: int
                Number of threads to use in parallel execution
        ''''
        self.dr         = domain.dr
        self.dk         = domain.dk
        self.rmax       = domain.length*domain.dr
        self.rmaxsq = self.rmax*self.rmax
        self.num_threads = nthreads if nthreads is not None else multiprocessing.cpu_count()
        self.num_bins = int(domain.length)

    def chunk(self,int num_indices, int num_chunks):
        cdef cIntType[:,:] chunked_indices = np.zeros((num_chunks,2),dtype=cIntType)
        index_list = range(num_indices)
        len_index_list = len(index_list)
        chunk_size = int(ceil(len_index_list/float(num_chunks)))
        full_list = [index_list[i:i+chunk_size] for i in range(0,len_index_list,chunk_size)]
        for i,chunk in enumerate(full_list):
            chunked_indices[i,0] = chunk[0]
            chunked_indices[i,1] = chunk[-1]+1
        return np.array(chunked_indices)

    def calc(self,
                     cFloatType [:,:,:] positions1,
                     cFloatType [:,:,:] positions2,
                     cFloatType [:,:] box,
                     bint selfHist):

        cdef cIntType frame,k
        cdef cFloatType[:,:] R1, R2

        cdef cFloatType imax = positions1.shape[1]
        cdef cFloatType jmax = positions2.shape[1]

        cdef bint intraHist = selfHist

        cdef cIntType[:,:] chunks        = self.chunk(imax,self.num_threads)
        cdef cFloatType[:,:] Base2D      = np.zeros((self.num_threads,self.num_bins), dtype=floatType)
        cdef cFloatType[:,:] thread_hist = np.zeros((self.num_threads,self.num_bins), dtype=floatType)
        cdef cFloatType[:] Base1D        = np.zeros(self.num_bins, dtype=floatType)
        cdef cFloatType[:] hist          = np.zeros(self.num_bins, dtype=floatType)
        cdef cFloatType[:] frame_hist    = np.zeros(self.num_bins, dtype=floatType)
        cdef cFloatType[:] L             = np.zeros(3, dtype=floatType)

        cdef int count = 0
        for frame in range(positions1.shape[0]):
            count += 1

            R1 = positions1[frame]
            R2 = positions2[frame]
            L[0] = box[frame]
            L[1] = box[frame]
            L[2] = box[frame]

            # need to "reset" these arrays for each loop
            frame_hist[:]    = Base1D
            thread_hist[:,:] = Base2D

            self.calculate(r1,r2,imax,jmax,BOXL,frame_hist,thread_hist,chunks,selfHist)
            for k in range(self.num_bins):
                hist[k] += frame_hist[k]

        for k in range(self.num_bins):
            hist[k] += hist[k]/count

        return np.array(hist)

    cdef void calculate(self,
                             cFloatType[:,:] R1, 
                             cFloatType[:,:] R2, 
                             cIntType imax,
                             cIntType jmax,
                             cFloatType[:] L,
                             cFloatType[:] hist,
                             cFloatType[:,:] thread_hist,
                             cIntType[:,:] chunks,
                             bint selfHist) nogil:
        cdef cFloatType num_pairs
        cdef cFloatType lx  = L[0]
        cdef cFloatType lx2 = L[0]/2.0
        cdef cFloatType ly  = L[1]
        cdef cFloatType ly2 = L[1]/2.0
        cdef cFloatType lz  = L[2]
        cdef cFloatType lz2 = L[2]/2.0
        cdef cFloatType dx,dy,dz,r,rsq,k
        
        # loop indices for position indices
        cdef Py_ssize_t i,j,i0,i1,j0,j1

        # loop indices for wavenumber index
        cdef Py_ssize_t q

        cdef Py_ssize_t thread_num
        cdef Py_ssize_t pair_count = 0;


        for thread_num in prange(self.num_threads, 
                                 schedule='static',
                                 chunksize=1):

            i0 = chunks[thread_num,0]

            # If selfHist, we don't want to double count.
            if selfHist and thread_num == self.num_threads - 1:
                i1 = chunks[thread_num,1] - 1
            else:
                i1 = chunks[thread_num,1]

            for i in range(i0,i1):

                # If selfHist, we don't want to double count.
                if selfHist:
                    j0 =i+1;
                else:
                    j0 =0

                for j in range(j0,jmax):
                    dx=c_fabs(r1[i,0] - r2[j,0])
                    dy=c_fabs(r1[i,1] - r2[j,1])
                    dz=c_fabs(r1[i,2] - r2[j,2])
        
                    # apply periodic boundary condition
                    if dx>lx2:
                        dx=dx-lx
                    if dy>ly2:
                        dy=dy-ly
                    if dz>lz2:
                        dz=dz-lz
        
                    rsq = dx*dx + dy*dy + dz*dz
                    if rsq<self.rmaxsq:
                        r = c_sqrt(rsq) #only take sqroot if we must
                        for q in range(0,self.num_bins):
                            k = self.dk*(q+1);
                            thread_hist[thread_num,q] = thread_hist[thread_num,q] + c_sin(k*r)/r
                            pair_count += 1
        


        # sum all thread histograms into master histogram (gather)
        for thread_num in range(self.num_threads):
            for q in range(self.num_bins):
                hist[q] = hist[q] + thread_hist[thread_num,q]


        # rescale and shift each wavenumber
        for q in range(0,self.num_bins):
            k = self.dk*(q+1);
            hist[q]=hist[q]/(k*pair_count);
            if selfHist:
                hist[q] = 2*hist[q] + 1
