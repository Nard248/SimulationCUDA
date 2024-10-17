# distutils: language = c++
# cython: language_level=3
import numpy as np
cimport numpy as np
# Import C++/CUDA declarations
cdef extern from "parameters.h":
    struct Params:
        pass

    Params initialize_parameters(tuple, tuple, tuple, tuple)
    void compute_myu(Params&)
    void compute_state_raw(double* d_myu_real, double* d_myu_imag, Params&)
    void print_parameters(const Params&)
    void free_parameters(Params&)

cdef class PyParams:
    cdef Params params

    def __cinit__(self, tuple d, tuple N, tuple myu_size, tuple myu_mstd):
        self.params = initialize_parameters(d, N, myu_size, myu_mstd)

    def compute_myu(self):
        compute_myu(self.params)

    # Declare the expected NumPy type (double) for d_myu_real and d_myu_imag
    # The "ndim=1" ensures it's a 1D array, "dtype=np.float64" ensures it's a double array.
    def compute_state(self, np.ndarray[np.float64_t, ndim=1] d_myu_real, np.ndarray[np.float64_t, ndim=1] d_myu_imag):
        assert d_myu_real.shape[0] == d_myu_imag.shape[0], "Real and Imaginary arrays must be the same size"

        # Get the size of the arrays
        cdef int size = d_myu_real.shape[0]

        # Get pointers to the data
        cdef double * real_ptr = <double *> d_myu_real.data
        cdef double * imag_ptr = <double *> d_myu_imag.data

        # Call the C++ function
        compute_state_raw(real_ptr, imag_ptr, self.params)

    def print_parameters(self):
        print_parameters(self.params)

    def free(self):
        free_parameters(self.params)
