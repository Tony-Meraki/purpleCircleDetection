# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = "heatmapper",
    version = "1.0.0",
    keywords = ("heatmap"),
    description = "Python library for creating heatmap",
    license = "MIT Licence",

    url = "https://github.com/luckcul/heatmapper",
    author = "luckcul",
    author_email = "tyfdream@gmail.com",

    packages = ['heatmapper'],
    platforms = "any",
    install_requires = ['pillow']
)