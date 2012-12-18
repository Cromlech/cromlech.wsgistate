# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version = '0.1dev'

install_requires = [
    'wsgistate',
    'setuptools',
    'transaction',
    ]

tests_require = [
    'WebTest',
    ]

setup(name='cromlech.wsgistate',
      version=version,
      description="Session handling for cromlech using wsgistate",
      long_description=(
          open("README.txt").read() + "\n" +
          open(os.path.join("src", "cromlech", "wsgistate",
                            "test_session.txt")).read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Cromlech Wsgistate Session',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org/',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['cromlech',],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_filter_factory]
      session_wrapper = cromlech.wsgistate.middleware:session_wrapper
      """,
      )
