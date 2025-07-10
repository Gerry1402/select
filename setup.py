from setuptools import setup, find_packages

setup(
    name="select_options",
    version="0.1.0",
    author="Gerard Vello",
    author_email="gerard.vello@gmail.com",
    description="A simple library for creating interactive selection menus in terminal applications.",
    long_description="A simple library for creating interactive selection menus in terminal applications. It is concieved as a library for personal use, but I'm open to proposals.",
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