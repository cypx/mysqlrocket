#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
import mysqlrocket
 
setup(
    name='mysqlrocket',
    version='0.0.3',
    packages=find_packages(),
    author="Cyprien Devillez",
    author_email="cyp@bidouille.info",
    description="Simple CLI tool to create, delete and dump easily MySQL databases",
    long_description=open('README.rst').read(),
    include_package_data=True,
    url='https://github.com/cypx/mysqlrocket',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
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
    license="GPL",
 
) 
