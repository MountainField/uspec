# -*- coding: utf-8 -*-

# =================================================================
# uspec
#
# Copyright (c) 2020 Takahide Nogayama
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# =================================================================

import io
from setuptools import setup

if __name__ == "__main__":
    
    # Loading __version__, __author__, etc
    pycode4meta = ""
    with io.open("src/uspec.py", "rt", encoding="UTF-8") as f:
        for line in f:
            if line.startswith("__"):
                pycode4meta += line
    exec(pycode4meta)
    
    _long_description=__description__
    with io.open("README.md", "rt", encoding="UTF-8") as f:
        _long_description = f.read()
    
    setup(
        name="uspec",
        version=__version__,
        description=__description__,
        author=__author__,
        author_email=__author_email__,
        url=__url__,
        download_url=__download_url__,
        license=__license__,
        
        long_description=_long_description,
        long_description_content_type="text/markdown",
        
        python_requires='>=3.0',
        
        package_dir={
            "": "src"
            },
        py_modules=[
            "uspec",
            ],
        scripts=[
            "scripts/uspec",
            ],
        test_suite="tests",
        
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Documentation",
            "Topic :: Software Development :: Documentation",
            "Topic :: Software Development :: Quality Assurance",
            "Topic :: Software Development :: Testing",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
      ],
    )
