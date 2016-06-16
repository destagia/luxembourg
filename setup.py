# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="luxembourg",
    version="0.1.0",
    description="A pip package",
    license="MIT",
    author="Shohei Miyashita",
    packages=find_packages(),
    install_requires=['bottle', 'chainer'],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ]
)
