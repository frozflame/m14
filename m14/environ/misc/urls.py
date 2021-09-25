#!/usr/bin/env python3
# coding: utf-8

import urllib.parse
from urllib.parse import ParseResult


def parse_qs_flat(query: str):
    d = urllib.parse.parse_qs(query, keep_blank_values=True)
    return {k: v[0] for k, v in d.items()}


def parse_url(url) -> (ParseResult, dict):
    pr = urllib.parse.urlparse(url)
    d = parse_qs_flat(pr.query)
    return pr, d


def parse_url_to_dict(url, component_prefix='@') -> dict:
    pr = urllib.parse.urlparse(url)
    d = parse_qs_flat(pr.query)
    # noinspection PyProtectedMember
    d.update({component_prefix + k: v for k, v in pr._asdict().items()})
    return d
