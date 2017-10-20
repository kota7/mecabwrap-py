# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='mecabwrap',
    version='0.1',
    description='A wrapper for MeCab morphological analyzer',
    author='Kota Mori', 
    author_email='kmori05@gmail.com',
    url='https://github.com/kota7/mecabwrap',
    
    packages=['mecabwrap'],
    install_requires=[],
    package_data={},
    entry_points={},
    
    test_suite='tests'
)
