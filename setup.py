#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
__author__ = "Cyprien Devillez"
__license__ = "GPL"
__version__ = "0.0.9"
__description__ = "Simple CLI tool to create and delete easily MySQL databases."
 
setup(
    name='mysqlrocket',
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email="cyp@bidouille.info",
    description=__description__,
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=['appdirs','MySQL-python'],
    url='https://github.com/cypx/mysqlrocket',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
    ],
    entry_points = {
        'console_scripts': [
            'mysqlrocket = mysqlrocket.mysqlrocket:launcher',
        ],
    },
    license=__license__,
 
) 
