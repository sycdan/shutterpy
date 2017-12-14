from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name='shutterpy',
    version='0.1.0',
    description="A simple self-hosted photo album.",
    long_description=long_description,
    url='https://github.com/sycdan/shutterpy',
    author='sycdan',
    py_modules=['shutterpy'],
    install_requires=install_requires,
)
