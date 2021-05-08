# Cython compile instructions
"""
Cython compilation instruction script for building the extension
mcss_ext2 containing the function simulation_results_vectorized
as described in the mcss_ext2.pyx file.
"""
try:
    from setuptools import setup
    from setuptools import Extension
    print("Using setuptools")
except:
    from distutils.core import setup, Extension
    print("Using disutils")

from Cython.Build import cythonize
import os
# Use python setup.py build_ext --inplace
# to compile

#os.environ["CC"] = "/usr/bin/gcc"

ext = Extension(
    "mcss_ext2",
    sources=["mcss_ext2.pyx", "mcss.cpp"],
    extra_compile_args=["-std=c++11"],

)

setup(name="cython_mcss", ext_modules=cythonize(ext, language_level="3"))
