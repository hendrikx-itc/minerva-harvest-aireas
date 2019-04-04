# -*- coding: utf-8 -*-

from setuptools import setup

__author__ = "Hendrikx ITC"

setup(
    name="minerva-harvest-aireas",
    description='Minerva harvest plugin for aireas json data',
    version="1.0.0",
    description=__doc__,
    author=__author__,
    author_email='info@hendrikx-itc.nl',
    python_requires='>=3.5',
    install_requires=["minerva"],
    packages=["minerva_harvest_aireas"],
    package_dir={"": "src"},
    entry_points={
        "minerva.harvest.plugins": ["aireas = minerva_harvest_aireas:Plugin"],
        "minerva.data_generator": [
            "aireas = minerva_harvest_aireas.generate:generate"
        ]
    }
)
