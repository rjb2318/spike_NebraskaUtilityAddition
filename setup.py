#!/usr/bin/env python 
# encoding: utf-8

"""
setup.py

"""
import setuptools
# version.py defines static version names
#from .version import version
#from .version import revision
#from .version import ProgramName
import re

_version_re = re.compile(r"version\s+=\s+'(.*)'")
_rev_re = re.compile(r"revision\s+=\s+'(.*)'")

with open('spike/version.py', 'rb') as f:
    F = f.read()
    version = str(_version_re.search(F.decode('utf-8')).group(1))
print("version :",version)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spike_py',
    version=version,
    author="M-A. Delsuc",
    author_email="madelsuc@unistra.fr",
    description="The SPIKE program. A collaborative development for a FT-spectroscopy processing program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/delsuc/spike",
    packages=setuptools.find_packages(),
    license="CeCILL-2.1",
    provides=["spike"],
    requires=["matplotlib", "numpy", 'scipy', 'tables'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry"
    ],
)

# How-To
# python QC.py
# cd spike; python dev_setup.py
# doc/script_doc.sh
# python3 setup.py sdist
# rsync -av spikedoc/* /media/web/CASC4DE/softwares/spike/spikedoc    
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# conda create -n test999 numpy scipy matplotlib pytables pandas
# conda activate test999
# conda install ipympl
# pip install --extra-index-url https://testpypi.python.org/pypi spike-py
# python -m spike.Tests -D /DATA/DATA_test
# twine upload  dist/*

