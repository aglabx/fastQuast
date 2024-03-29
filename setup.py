#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 25.03.2023
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
"""Setup script for fastQuast."""
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='fastQuast',
    version='1.0.2',
    description='Fast and simple Quality Assessment Tool for Large Genomes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Aleksey Komissarov',
    author_email='ad3002@gmail.con',
    url='https://github.com/aglabx/fastQuast',
    packages=find_packages(),
    install_requires=[
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'fastQuast=fastQuast.fastQuast:main',
            'fastquast=fastQuast.fastQuast:main',
        ],
    },
)
