# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='mecabwrap',
    version='0.3.0',
    description='Yet another interface to MeCab morphological analyzer',
    author='Kota Mori', 
    author_email='kmori05@gmail.com',
    url='https://github.com/kota7/mecabwrap-py',
    download_url='https://github.com/kota7/mecabwrap-py/archive/0.1.5.tar.gz',

    packages=['mecabwrap'],
    install_requires=[],
    test_require=['pandas', 'numpy'],
    package_data={},
    entry_points={},
    
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Natural Language :: Japanese',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'        
    ],
    test_suite='tests'
)
