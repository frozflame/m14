#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os

from joker.default import under_home_dir

_rootdir = None


def _get_rootdir():
    global _rootdir
    if _rootdir is None:
        path = under_home_dir('.m14', 'relocate.txt')
        if os.path.isfile(path):
            _rootdir = open(path).read().strip()
        else:
            _rootdir = under_home_dir('.m14')
    return _rootdir


def under_default_dir(package, *paths):
    if isinstance(package, str):
        name = package.split('.')[-1]
    else:
        name = package.__name__.split('.')[-1]
    return os.path.join(_get_rootdir(), name, *paths)
