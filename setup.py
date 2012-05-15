#!/usr/bin/env python

from setuptools import setup

setup(
    name='agilezensync',
    version='0.1',
    description='One-way sync to AgileZen',
    author='Anthony Johnson',
    author_email='aj@ohess.org',
    url='http://github.com/agjohnson/agilezen-sync',
    namespace_packages=['agilezensync'],
    packages=['agilezensync'],
    install_requires=[
        'requests',
        'slumber>=0.4.2dev-agjohnson'
    ],
    dependency_links=[
        'http://github.com/agjohnson/slumber#egg=slumber-0.4.2dev-agjohnson'
    ],
    entry_points={
      'console_scripts': [
        'agilzensync = agilezensync.storage:sync',
      ]
    },
    zip_safe=False,
    #test_suite='agilezensync.tests'
)
