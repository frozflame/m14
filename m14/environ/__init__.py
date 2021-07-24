#!/usr/bin/env python3
# coding: utf-8

__version__ = '0.4.2'

import os

import volkanic
from volkanic.environ import GIMixinDirs


class GlobalInterface(volkanic.GlobalInterface, GIMixinDirs):
    package_name = 'm14.environ'

    def under_data_dir(self, *paths, mkdirs=False):
        if 'data_dir' not in self.conf:
            ddr = self.conf.get('m14_ddr', '/data/local')
            name = self.package_name.split('.')[-1]
            data_dir = os.path.join(ddr, name)
            self.conf.setdefault('data_dir', path)
        return super().under_data_dir(*paths, mkdirs=mkdirs)


if __name__ == '__main__':
    print(__version__)
