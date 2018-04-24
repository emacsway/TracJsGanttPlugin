#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2014 Chris Nelson <Chris.Nelson@SIXNET.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from setuptools import setup

setup(
    name='Trac-jsGantt',
    author='Chris Nelson',
    author_email='Chris.Nelson@SIXNET.com',
    description='Trac plugin displaying jsGantt charts in Trac',
    version='1.2.0.0',
    url='https://trac-hacks.org/wiki/TracJsGanttPlugin',
    license='3-Clause BSD',
    packages=['tracjsgantt'],
    package_data={'tracjsgantt': ['htdocs/*.js', 'htdocs/*.css']},
    entry_points={
        'trac.plugins': [
            'tracjsgantt = tracjsgantt'
        ]
    }
)
