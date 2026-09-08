"""
LitPro - Setup Configuration

Setup script for installing the LitPro package.
"""
from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="lpmd",
    version="1.0.0",
    author="Abhishek Shivakumar",
    author_email="abhishek@example.com",
    description="LitPro - Modern literate programming framework for any language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/godofecht/lpmd",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Typing :: Typed",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'litpro=core.litpro_cli:main',
        ],
    },
    keywords='literate-programming, markdown, python, documentation, executable-documentation, jupyter-alternative, multi-language',
    project_urls={
        'Documentation': 'https://github.com/godofecht/lpmd#readme',
        'Source': 'https://github.com/godofecht/lpmd',
        'Tracker': 'https://github.com/godofecht/lpmd/issues',
    },
)
