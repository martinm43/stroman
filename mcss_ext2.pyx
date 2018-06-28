# distutils: language = c++
# distutils: sources = mcss.cpp

# Cython interface file for wrapping the object
#

cimport mcss_ext

from libcpp.vector cimport vector
from libcpp.string cimport string


# c++ interface to cython
def simulations_result_vectorized(head_to_head, future_games):
    return mcss_ext.simulations_result_vectorized(head_to_head, future_games)

