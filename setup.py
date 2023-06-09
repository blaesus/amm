from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="amm",
    version="0.0.1",
    author="Andy Shu",
    author_email="shu@immux.com",
    description="AI Model Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blaesus/amm",
    packages=['src/amm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
