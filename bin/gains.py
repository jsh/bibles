#!/usr/bin/env python
"""How much can snippet compression learn from different bases?"""

from collections import namedtuple
import logging
import os
import zlib

import parseargs
import sizes
from sizes import Sizes

BASE_DIR = "ot.d"
SNIPPET_DIR = "nt.d"


Chunk = namedtuple("Chunk", "name, text")


def teaching_gain(base_size, snippet_size, combined_size):
    """Gain in compression through teaching.
    Scaled to make the numbers easy to read.

    >>> teaching_gain(100, 10, 109)
    1
    >>> teaching_gain(100, 10, 111)
    -1
    """
    taught_snippet_size = combined_size - base_size
    gain = snippet_size - taught_snippet_size
    fmt = (
        "base_size = %d, "
        "snippet_size = %d, "
        "combined_size = %d, "
        "teaching_gain = %d"
    )
    logging.debug(fmt, base_size, snippet_size, combined_size, gain)

    return round(gain)


def snippet_gain(base, snippet):
    """Gain from compressing snippet after teaching."""
    base_sizes = Sizes(BASE_DIR)
    snippet_sizes = Sizes(SNIPPET_DIR)
    combined_size = len(zlib.compress(base.text + snippet.text))
    return teaching_gain(
        base_sizes.size(base.name), snippet_sizes.size(snippet.name), combined_size
    )


def main():
    """The feature attraction."""
    args = parseargs.parseargs()
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))

    base_names = [file for file in os.listdir(BASE_DIR) if sizes.not_json(file)]
    snippet_names = [file for file in os.listdir(SNIPPET_DIR) if sizes.not_json(file)]

    column_headers = [""] + snippet_names
    print(",".join(column_headers))

    for base_name in base_names:
        row = [base_name]
        with open(os.path.join(BASE_DIR, base_name), "rb") as bfd:
            base = Chunk(name=base_name, text=bfd.read())
        for snippet_name in snippet_names:
            with open(os.path.join(SNIPPET_DIR, snippet_name), "rb") as sfd:
                snippet = Chunk(name=snippet_name, text=sfd.read())
            row.append(str(snippet_gain(base, snippet)))

        print(",".join(row))


if __name__ == "__main__":
    main()
