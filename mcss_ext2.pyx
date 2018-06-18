# distutils: language = c++
# distutils: sources = mcss.cpp

# Cython interface file for wrapping the object
#

cimport mcss_ext

# c++ interface to cython
def simulations_results_vectorized():
    return mcss_ext.simulations_results_vectorized()
