##############################################################################
#
# Copyright (c) 2010 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import os

from setuptools import setup
#from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'SQLAlchemy',
    'zope.sqlalchemy']

tests_require = [
    "transaction",
    ]

entry_points = """
"""

setup(name='pyramid_sqla',
      version='1.0rc2',
      description='A SQLAlchemy library for Pyramid applications',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pylons",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database",
        ],
      keywords='web wsgi pylons pyramid',
      author="Mike Orr",
      author_email="sluggoster@gmail.com",
      url="http://docs.pylonshq.com",
      license="MIT",
      py_modules=["pyramid_sqla"],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires = ["SQLAlchemy", "zope.sqlalchemy"],
      test_suite="pyramid_sqla",
      entry_points=entry_points,
      )

