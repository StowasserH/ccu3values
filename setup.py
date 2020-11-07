# -*- coding: utf-8 -*-
# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ccu3values',
    version='0.1.0',
    description='Reads values form a ccu3 via XMLRPC',
    long_description=readme,
    author='Harald Stowasser',
    author_email='git@stowasser.tv',
    url='https://github.com/StowasserH/ccu3values',
    license=license,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
    python_requires='>=3.6'
)
