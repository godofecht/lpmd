"""
Literate Python Markdown (LPMD) - Setup Configuration

Setup script for installing the LPMD package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="lpmd",
    version="1.0.0",
    author="Abhishek Shivakumar",
    author_email="abhishek@example.com",
    description="Literate Python Markdown - A revolutionary literate programming framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhishekshivakumar/lpmd_project",
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
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'lpmd-execute=core.lpmd_executor:main',
            'lpmd-generate-html=core.lpmd_html_generator:main',
        ],
    },
    keywords='literate-programming, markdown, python, documentation, executable-documentation',
    project_urls={
        'Documentation': 'https://github.com/abhishekshivakumar/lpmd_project#readme',
        'Source': 'https://github.com/abhishekshivakumar/lpmd_project',
        'Tracker': 'https://github.com/abhishekshivakumar/lpmd_project/issues',
    },
)