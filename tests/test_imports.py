#!/usr/bin/env python3
# coding: utf-8

from joker.environ.utils import load_modules_under_dir

from m14.environ import GlobalInterface

gi = GlobalInterface()


def test_module_imports():
    load_modules_under_dir(
        gi.under_project_dir(),
        'm14.', 'tests.'
    )


if __name__ == '__main__':
    test_module_imports()
