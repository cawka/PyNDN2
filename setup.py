# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from setuptools import setup, find_packages

setup(
    name = "PyNDN",
    version = "2.0a3",
    license = "BSD",
    url = "https://github.com/named-data/PyNDN2",

    description = ("PyNDN: An Named Data Networking client library with TLV wire "
                   "format support in native Python"),

    packages = find_packages("python"),
    package_dir = {"":"python"},

    install_requires = ['pycrypto',
                        'trollius'],

    maintainer = "Alexander Afanasyev",
    maintainer_email = "alexander.afanasyev@ucla.edu",
)
