import setuptools
from distutils.core import setup

setup(
    name="Actiwatch",
    version="0.1.2",
    author="Ryan Opel",
    author_email="ryan.a.opel@gmail.com",
    description="Actiwatch is a Python module built for interacting with Philips Actiwatch actigraphy devices.",
    long_description=open("README.md").read(),
    url="",
    packages=setuptools.find_packages(),
    license="LICENSE",
    install_requires=["pandas >= 0.23.0", "astral == 1.6.1", "numpy == 1.15.1"],
)
