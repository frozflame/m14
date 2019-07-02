#!/usr/bin/env python3
# coding: utf-8


import time


def tindex(sequence, period, count=None):
    n = len(sequence)
    idx = int(time.time() / period)
    if not count:
        return sequence[idx % n]
    count = min(n, count)
    idx = idx * count
    return [sequence[i % n] for i in range(idx, idx + count)]
