# distutils: language = c++
# distutils: sources = mcss.cpp

# Cython interface file for wrapping the object
#
#

from libcpp.vector cimport vector

# c++ interface to cython
cdef extern from "mcss.h":
    vector[vector[double]] simulations_result_vectorized()
