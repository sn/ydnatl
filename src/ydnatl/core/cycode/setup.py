from setuptools import setup, Extension
from Cython.Build import cythonize
import os

ext = Extension(
    name="cython_render",
    sources=[os.path.abspath("cython_render.pyx")],
)

setup(
    ext_modules=cythonize([ext]),
)