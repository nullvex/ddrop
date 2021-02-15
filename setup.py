#!/usr/bin/env python3

import os
from setuptools import setup

# get key package details from py_pkg/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'ddrop', '0.1')) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open('README.md', 'r') as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name=about['ddrop'],
    description=about['ddrop - ddrop shares files in a multipart/multicloud and encrypted fashion'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['0.1'],
    author=about['nullvex'],
    author_email=about['null@nullvex.com'],
    url=about['nullvex.com'],
    packages=['ddrop'],
    include_package_data=True,
    python_requires=">=3.7.*",
    install_requires=['', ''],
    license=about['Apache 2.0'],
    zip_safe=True,
    entry_points={
        'console_scripts': ['ddrop=ddrop.entry_points:main'],
    },
    classifiers=[
        'Development Status :: 2 - alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='distributed dead file drop '
)
