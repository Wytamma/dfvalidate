# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='dfvalidate',
    version='0.1.0',
    description='Validate the foramt and values of a pandas data frame',
    long_description=readme,
    author='Wytamma Wirth',
    author_email='wytamma.wirth@me.com',
    url='https://github.com/wytamma/dfvalidate',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
