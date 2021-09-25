#!/usr/bin/env python3
# coding: utf-8

import importlib
import re
from datetime import timedelta

from srt import TimestampParseError
from volkanic.introspect import find_all_plain_modules
from volkanic.utils import printerr


def parse_time(time_string: str):
    """
    >>> parse_time('00:03:02,521')
    datetime.timedelta(seconds=182, microseconds=521000)
    """
    regex = re.compile('^([0-9]+):([0-9]+):([0-9]+),([0-9]+)$')
    match = regex.match(time_string)
    if match is None:
        raise TimestampParseError("Unparseable timestamp: {}".format(time_string))
    hrs, mins, secs, msecs = map(int, match.groups())
    return timedelta(hours=hrs, minutes=mins, seconds=secs, milliseconds=msecs)


def _check_prefix(dotpath, dotpath_prefixes):
    for prefix in dotpath_prefixes:
        if dotpath.startswith(prefix):
            return True
    return False


def load_all_modules(project_dir: str, *dotpath_prefixes):
    if not project_dir or not dotpath_prefixes:
        return
    for dotpath in find_all_plain_modules(project_dir):
        if _check_prefix(dotpath, dotpath_prefixes):
            printerr('importing', dotpath)
            importlib.import_module(dotpath)
