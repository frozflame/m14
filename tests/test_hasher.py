#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import hashlib
import os

from m14.legacy.hasher import HashedPath, guess_hash_algorithm


def test_hashed_path():
    path = os.path.abspath(__file__)

    hp1 = HashedPath.generate(path)
    assert hp1.verify()

    hp2 = HashedPath.parse(str(hp1))
    assert hp2.verify()

    hp3 = HashedPath.parse(path)
    assert hp3.verify()


def test_guess_hash_algorithm():
    algos = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
    for algo_name in algos:
        print("algo_name =", algo_name)
        h = hashlib.new(algo_name)
        assert guess_hash_algorithm(h.digest()) == algo_name
        assert guess_hash_algorithm(h.hexdigest()) == algo_name


if __name__ == "__main__":
    test_hashed_path()
    # test_hashed_password()
    test_guess_hash_algorithm()
