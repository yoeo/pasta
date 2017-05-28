#!/usr/bin/env python3

import pathlib

from setuptools import setup, find_packages


setup(
    name="pasta",
    author="yoeo",
    version="0.1",
    url="https://github.com/yoeo/pasta",
    license="MIT",
    description="Pretty Paste source code on Slack, language autodetected",
    install_requires=pathlib.Path('requirements.txt').read_text().splitlines(),
    packages=find_packages(),
    scripts=['bin/pasta-gunicorn'],
    entry_points={
        'console_scripts': ['pasta = pasta:main']
    },
)
