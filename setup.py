
from setuptools import setup, find_packages
from ddrop.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='ddrop',
    version=VERSION,
    description='Manages remote archives',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='nvx',
    author_email='null@nullvex.com',
    url='https://github.com/nullvex/ddrop',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'ddrop': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        ddrop = ddrop.main:main
    """,
)
