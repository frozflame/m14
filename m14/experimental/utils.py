#!/usr/bin/env python3
# coding: utf-8

import base64
import json
import os
import shlex
import sys
from functools import lru_cache

# TODO: drop this
from joker.textmanip.path import make_new_path
from volkanic.introspect import razor


def dump_json_request_to_curl(method: str, url: str, data=None, aslist=False):
    method = method.upper()
    if method == 'GET':
        parts = ['curl', url]
    else:
        parts = [
            'curl', '-X', method, url,
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(razor(data), ensure_ascii=False),
        ]
    if aslist:
        return parts
    parts = [shlex.quote(s) for s in parts]
    return ' '.join(parts)


@lru_cache(100)
def get_json_config(path):
    return json.load(open(path))


def copy_fields(record: dict, keys: list, keymap: dict, default=None):
    new_record = {k: record.get(k, default) for k in keys}
    for old_key, new_key in keymap.items():
        new_record[new_key] = record.get(old_key, default)
    return new_record


# Python 3.5+
if hasattr(bytes, 'hex'):
    def random_hex(size=12):
        return os.urandom(size).hex()
else:
    def random_hex(size=12):
        b = os.urandom(size)
        return base64.b16encode(b).decode('ascii')


def camel_case_split(name: str):
    # https://stackoverflow.com/a/29920015/2925169
    matches = re.finditer(
        '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', name
    )
    return [m.group(0) for m in matches]


def camel_case_to_underscore(name: str):
    return '_'.join(s.lower() for s in camel_case_split(name))


def text_routine_catstyle(func, *paths):
    # routine function for quick and dirty text manipulation scripts
    if not paths:
        paths = sys.argv[1:]

    if not paths:
        for line in sys.stdin:
            print(func(line))
        return
    for path in paths:
        for line in open(path):
            print(func(line))


def text_routine_perfile(func, ext='.out'):
    # routine function for quick and dirty text manipulation scripts
    for path in sys.argv[1:]:
        outpath = make_new_path(path, ext)
        func(path, outpath)
