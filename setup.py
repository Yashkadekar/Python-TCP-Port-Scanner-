"""
Setup script for Python Port Scanner
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="python-port-scanner",
    version="2.0.0",
    author="Cybersecurity Instructor (AI Assistant)",
    author_email="",
    description="Professional TCP/UDP port scanner with GUI",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python-port-scanner",
    py_modules=["scanner", "gui_scanner"],
    install_requires=[
        "tqdm>=4.65.0",
        "ttkbootstrap>=1.10.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "port-scanner=scanner:main",
            "port-scanner-gui=gui_scanner:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="port scanner security network tcp udp reconnaissance",
    project_urls={
        "Documentation": "https://github.com/yourusername/python-port-scanner",
        "Source": "https://github.com/yourusername/python-port-scanner",
        "Tracker": "https://github.com/yourusername/python-port-scanner/issues",
    },
)
