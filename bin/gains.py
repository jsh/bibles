#!/usr/bin/env python
"""How much can snippet compression learn from different bases?"""

from collections import namedtuple
from collections import defaultdict
import logging
import os
import zlib

import parseargs
import sizes
from sizes import Sizes

BASE_DIR = "ot.d"
SNIPPET_DIR = "nt.d"


Chunk = namedtuple("Chunk", "name, text")


def taught_size(base, snippet, base_sizes):
    """Size increase from adding snippet, then compressing."""
    combined_size = len(zlib.compress(base.text + snippet.text))
    return combined_size - base_sizes[base.name]


def main():
    """The feature attraction."""
    args = parseargs.parseargs()
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))

    base_names = sorted([file for file in os.listdir(BASE_DIR) if sizes.not_json(file)])
    snippet_names = sorted(
        [file for file in os.listdir(SNIPPET_DIR) if sizes.not_json(file)]
    )

    logging.debug("base_names: %s", str(base_names))
    logging.debug("snippet_names: %s", str(snippet_names))

    column_headers = [""] + snippet_names
    print(",".join(column_headers))

    taught_sizes = defaultdict(dict)

    for base_name in base_names:
        base_sizes = Sizes(BASE_DIR).sizes()
        with open(os.path.join(BASE_DIR, base_name), "rb") as bfd:
            base = Chunk(name=base_name, text=bfd.read())
        for snippet_name in snippet_names:
            with open(os.path.join(SNIPPET_DIR, snippet_name), "rb") as sfd:
                snippet = Chunk(name=snippet_name, text=sfd.read())
            taught_sizes[base_name][snippet_name] = taught_size(
                base, snippet, base_sizes
            )

    for base_name in base_names:
        row = [base_name]
        self_size = taught_sizes[base_name][base_name]
        for snippet_name in snippet_names:
            row.append(str(taught_sizes[base_name][snippet_name] - self_size))
        print(",".join(row))


if __name__ == "__main__":
    main()
