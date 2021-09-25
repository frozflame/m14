#!/usr/bin/env python3
# coding: utf-8

from m14.environ import GlobalInterface
from m14.environ.utils import load_all_modules

gi = GlobalInterface()


def test_module_imports():
    load_all_modules(gi.under_project_dir(), 'm14.', 'tests.')


if __name__ == '__main__':
    test_module_imports()
