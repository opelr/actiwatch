from distutils.core import setup

setup(
    name="Actiwatch",
    version="0.1.0",
    author="Ryan Opel",
    author_email="ryan.a.opel@gmail.com",
    packages=["actiwatch", "actiwatch.tests"],
    license="LICENSE",
    description="Class for reading Philips Actiwatch data",
    long_description=open("README.md").read(),
    install_requires=["pandas >= 0.23.0", "astral == 1.6.1", "numpy == 1.15.1"],
)
