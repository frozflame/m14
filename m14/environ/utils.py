#!/usr/bin/env python3
# coding: utf-8

import fnmatch
import importlib
import logging
import re

from volkanic.introspect import find_all_plain_modules
from volkanic.utils import printerr


def multicheck(func, target, rules, positive_val: bool) -> bool:
    for rule in rules:
        if func(target, rule):
            return positive_val
    return not positive_val


def check_inclusive_prefixes(string: str, prefixes) -> bool:
    return multicheck(str.startswith, string, prefixes, True)


def check_exclusive_prefixes(string: str, prefixes) -> bool:
    return multicheck(str.startswith, string, prefixes, False)


def check_inclusive_patterns(string: str, patterns, case=True) -> bool:
    func = fnmatch.fnmatchcase if case else fnmatch.fnmatch
    return multicheck(func, string, patterns, True)


def check_exclusive_patterns(string: str, patterns, case=True) -> bool:
    func = fnmatch.fnmatchcase if case else fnmatch.fnmatch
    return multicheck(func, string, patterns, False)


def _regex_search(string: str, regex: str):
    return re.search(regex, string)


def check_inclusive_regexes(string: str, patterns) -> bool:
    return multicheck(_regex_search, string, patterns, True)


def check_exclusive_regexes(string: str, patterns) -> bool:
    return multicheck(_regex_search, string, patterns, True)


# deprecated. use check_{inclusive,exclusive}_* functions
def check_prefixes(string: str, include=None, exclude=None) -> bool:
    """
    Args:
        string (str): string to be checked
        include: None = include anything
        exclude: None = no exlusion rule
    """
    if exclude is not None:
        for prefix in exclude:
            if string.startswith(prefix):
                return False
    if include is not None:
        for prefix in include:
            if string.startswith(prefix):
                return True
        return False
    else:
        return True


def load_all_modules(project_dir: str, *dotpath_prefixes):
    if not project_dir or not dotpath_prefixes:
        return
    for dotpath in find_all_plain_modules(project_dir):
        if check_inclusive_prefixes(dotpath, dotpath_prefixes):
            printerr('importing', dotpath)
            importlib.import_module(dotpath)


def easylog(level):
    root = logging.root
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root.setLevel(level)
    root.addHandler(handler)


def read_lines(path: str):
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        yield line
