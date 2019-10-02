#!/usr/bin/env python
"""Canonicalize text.

Remove diacriticals.
Remove punctuation
Convert all text to lower-case.
"""

import string
import sys

import unidecode

nbytes = int(sys.argv[1])
s = sys.stdin.read(round(nbytes * 1.1))  # read in a little extra

table = str.maketrans({key: None for key in string.punctuation})
s = s.translate(table)

try:
    s = unidecode.unidecode(s).lower()
    assert len(s) >= nbytes
    print(s[: nbytes - 1])
except Exception:
    pass
