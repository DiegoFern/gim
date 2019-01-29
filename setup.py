from distutils.core import setup, Extension
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
from collections import OrderedDict

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

    
setup(
    name = "gim",
    version = "0.0.4",
    author = "DiegoFern",
    #author_email = "andrewjcarter@gmail.com",
    description = (""),
    license = "BSD",
    keywords = "",
    packages=['gim'],
    long_description=('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

