from setuptools import find_packages, setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("./*.pyx")
)
