# Cython compile instructions

from distutils.core import setup, Extension
from Cython.Build import cythonize

# Use python setup.py build_ext --inplace
# to compile

ext = Extension("mcss",sources=["mcss_ext2.pyx","mcss.cpp"])

setup(
  name = "cython_mcss",
  ext_modules = cythonize(ext),
  extra_compile_args=['-O3','-larmadillo','-lsqlite3','-I/Documents/sports_stats/naismith/.']
)
