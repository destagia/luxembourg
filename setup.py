# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

long_description = open("README.md").read()

setup(
    name="luxembourg",
    version="0.1.0",
    description="Game of last one AI learning",
    license="MIT",
    author="Shohei Miyashita",
    packages=find_packages(),
    install_requires=[
        'bottle==0.12.9',
        'chainer==1.9.1'
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ]
)
