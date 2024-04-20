#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from setuptools import Extension, setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")
from Cython.Build import cythonize

setup(
    name='pysettrie',
    url='https://github.com/GregoryMorse/pysettrie',
    version='1.0.2',
    author='Gregory Morse and Márton Miháltz',
    description='Efficient storage and querying of sets of sets using the trie data structure',
    packages=['settrie'],
    #install_requires=['sortedcontainers'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'],
    ext_modules = cythonize([
        Extension("settrie", ["settrie/settrie.pyx"], language="c++", extra_compile_args=["-std=c++14"])],
        language_level=3
    ), #"settrie.pyx")
    package_data = {
        'settrie': ['settrie*.pyd','settrie.pyx'],
    },
)
