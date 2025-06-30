from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="select_options",
    version="0.1.0",
    author="Gerard Vello",
    author_email="gerard.vello@gmail.com",
    description="A simple library for creating interactive selection menus in terminal applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "textual",
    ],
)