# Cython compile instructions

from distutils.core import setup
from Cython.Build import cythonize

# Use python setup.py build_ext --inplace
# to compile

setup(
  name = "mcss",
  ext_modules = cythonize('*.pyx'),
  extra_compile_args=['-O3','-larmadillo','-lsqlite3','-I/Documents/sports_stats/naismith/.']
)
