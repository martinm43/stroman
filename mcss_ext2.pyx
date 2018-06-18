# distutils: language = c++
# distutils: sources = mcss.cpp

# Cython interface file for wrapping the object
#

cimport mcss_ext

# c++ interface to cython
def simulations_result_vectorized():
    return mcss_ext.simulations_result_vectorized()
