#!/usr/bin/env python3
"""
Setup script for Motion Relay Controller

This script allows easy installation of the motion relay controller package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Motion Relay Controller - A Python-based system for controlling relay modules and PIR motion sensors using Raspberry Pi GPIO pins."

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['RPi.GPIO>=0.7.0']

setup(
    name="motion-relay-controller",
    version="1.0.0",
    author="Motion Relay Controller",
    author_email="",
    description="A Python-based object-oriented system for controlling relay modules and PIR motion sensors using Raspberry Pi GPIO pins",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Home Automation",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "motion-relay-test=motion_relay_controller.test_system:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="raspberry-pi gpio motion-sensor relay automation home-automation",
    project_urls={
        "Bug Reports": "",
        "Source": "",
        "Documentation": "",
    },
)
