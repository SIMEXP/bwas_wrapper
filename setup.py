from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bwas_wrapper",
    version="0.1",
    description="A wrapper for the BWAS library",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Optional (see note above)
    project_urls={  # Optional
        "Bug Reports": "https://github.com/simexp/bwas_wrapper/issues",
        "Source": "https://github.com/simexp/bwas_wrapper",
    },
    packages= find_packages(),
    maintainer="Pierre Bellec",
    maintainer_email="pierre.bellec@gmail.com",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "nilearn",
        "joblib",
        "PyPDF2",
        "pandas"
    ],  # external packages as dependencies
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.5",
)
