#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

exec(open("mysqlrocket/ressources.py").read())

setup(
    name=__app_name__,
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=open("README.rst").read(),
    include_package_data=True,
    install_requires=[
        "appdirs",
        'configparser;python_version<"3"',
        'future;python_version<"3"',
        'MySQL-python;python_version<"3"',
        'mysqlclient;python_version>="3"',
        "argparse",
    ],
    url="https://github.com/cypx/mysqlrocket",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    entry_points={
        "console_scripts": ["mysqlrocket = mysqlrocket.mysqlrocket:launcher"]
    },
    license=__license__,
)
