from setuptools import setup, find_packages

with open("README.rst", "r") as read_me:
    long_description = read_me.read()


setup(
    name="DLTN Technical Documentation Generator",
    description="a generator for DLTN's technical documentation",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    version="0.0.1",
    author="Mark Baggett",
    author_email="mbagget1@utk.edu",
    maintainer_email="mbagget1@utk.edu",
    url="https://github.com/DigitalLibraryofTennessee/dltn_docs_generator",
    packages=find_packages(),
    install_requires=[
        "requests>=2.2.1",
        "repox>=0.0.2",
        "pyyaml>=4.2b4",
        "tqdm>=4.28.1",
        "emoji>=0.5.1",
        "arrow>=0.12.1",
        "lxml>=4.3.0",
    ],
    extras_require={"docs": ["sphinx >= 1.4", "sphinxcontrib-napoleon >= 0.7"]},
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    keywords=["libraries", "dpla", "europeana", "aggregators"],
)
