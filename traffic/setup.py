import io
import sys

from os.path import dirname
from setuptools import setup, find_packages
from traffic import VERSION

sys.path.append(dirname(__file__))

requires = [
    x.strip() for x in
    io.open('requirements.txt')
]

setup(
    name="tcounter",
    version=VERSION,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['tcounter = traffic.main:main']
    },
    install_requires=requires,
    long_description=io.open('README.md').read()
)
