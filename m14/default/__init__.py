#!/usr/bin/env python3
# coding: utf-8

import os.path
import sys
import volkanic.environ

import yaml

__version__ = '0.2'
_conf = None


def _load_conf():
    from joker.default import under_home_dir
    paths = [under_home_dir('.m14-default.yml'), '/etc/m14-default.yml']
    for path in paths:
        if os.path.isfile(path):
            return yaml.safe_load(open(path))


def _get_default_prefix():
    if sys.platform.startswith('win'):
        return r'c:\data'
    return '/data'


def _get_conf():
    global _conf
    if _conf is None:
        _conf = _load_conf() or {}
    if 'default' not in _conf:
        _conf['default'] = _get_default_prefix()
    return _conf


def under_default_dir(package, *paths):
    conf = _get_conf()
    name = getattr(package, '__name__', str(package)).split('.')[-1]
    try:
        dir_ = conf[name]
    except LookupError:
        dir_ = os.path.join(conf.get('default'), name)
    return os.path.join(dir_, *paths)


class GlobalInterface(volkanic.environ.GlobalInterface):
    primary_name = 'm14_default'
    package_name = 'm14.default'
    default_data_dir = '/data/local/m14'

    @classmethod
    def get_data_dir(cls):
        envvar_name = cls._fmt_envvar_name('data_dir')
        try:
            return os.environ[envvar_name]
        except KeyError:
            return cls.default_data_dir

    @classmethod
    def under_data_dir(cls, *paths):
        return os.path.join(cls.get_data_dir(), *paths)

    @classmethod
    def _get_conf_search_paths(cls):
        """
        Make sure this method can be called without arguments.
        """
        return [cls.under_data_dir('config.json5')]