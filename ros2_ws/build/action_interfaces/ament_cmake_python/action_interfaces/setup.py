from setuptools import find_packages
from setuptools import setup

setup(
    name='action_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('action_interfaces', 'action_interfaces.*')),
)
