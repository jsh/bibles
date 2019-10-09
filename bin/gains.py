#!/usr/bin/env python
"""How much can snippet compression learn from different bases?"""
# pylint: disable=fixme

import logging
import os
import zlib

import parseargs
import sizes
from sizes import Sizes

BASE_DIR = "ot.d"
SNIPPET_DIR = "nt.d"


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


def snippet_gain(base, base_text, snippet, snippet_text):
    """Gain from compressing snippet after teaching."""
    base_sizes = Sizes(BASE_DIR)
    snippet_sizes = Sizes(SNIPPET_DIR)
    combined_size = len(zlib.compress(base_text + snippet_text))
    return teaching_gain(
        base_sizes.size(base), snippet_sizes.size(snippet), combined_size
    )


def main():
    """The feature attraction."""
    args = parseargs.parseargs()
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))

    bases = [file for file in os.listdir(BASE_DIR) if sizes.not_json(file)]
    snippets = [file for file in os.listdir(SNIPPET_DIR) if sizes.not_json(file)]

    column_headers = [""] + snippets
    print(",".join(column_headers))

    for base in bases:
        line = [base]

        with open(os.path.join(BASE_DIR, base), "rb") as bfd:
            base_text = bfd.read()
        for snippet in snippets:
            with open(os.path.join(SNIPPET_DIR, snippet), "rb") as sfd:
                snippet_text = sfd.read()
            # TODO: Make {name, text} into a named tuple.
            line.append(str(snippet_gain(base, base_text, snippet, snippet_text)))

        print(",".join(line))


if __name__ == "__main__":
    main()
