#!/usr/bin/env python
"""How much can snippet compression learn from different bases?"""
# pylint: disable=too-many-locals

from collections import namedtuple
from collections import defaultdict
import logging
import os
import zlib

import parseargs
import sizes
from sizes import Sizes


Chunk = namedtuple("Chunk", "name, text")


def taught_size(base, snippet, base_sizes):
    """Size increase from adding snippet, then compressing."""
    combined_size = len(zlib.compress(base.text + snippet.text))
    compressed_snippet_size = combined_size - base_sizes[base.name]
    logging.debug(
        (
            "base: %s, snippet: %s, base_size: %s, "
            "combined_size: %s, compressed_snippet_size: %s"
        ),
        base.name,
        snippet.name,
        base_sizes[base.name],
        combined_size,
        compressed_snippet_size,
    )
    return compressed_snippet_size


def main():
    """The feature attraction."""
    args = parseargs.parseargs()
    base_dir = args.base_dir
    snippet_dir = args.snippet_dir

    base_names = sorted([file for file in os.listdir(base_dir) if sizes.not_json(file)])
    snippet_names = sorted(
        [file for file in os.listdir(snippet_dir) if sizes.not_json(file)]
    )

    logging.debug("base_names: %s", str(base_names))
    logging.debug("snippet_names: %s", str(snippet_names))

    column_headers = [""] + snippet_names
    print(",".join(column_headers))

    taught_sizes = defaultdict(dict)

    for base_name in base_names:
        base_sizes = Sizes(base_dir).sizes()
        with open(os.path.join(base_dir, base_name), "rb") as bfd:
            base = Chunk(name=base_name, text=bfd.read())
        for snippet_name in snippet_names:
            with open(os.path.join(snippet_dir, snippet_name), "rb") as sfd:
                snippet = Chunk(name=snippet_name, text=sfd.read())
            taught_sizes[base_name][snippet_name] = taught_size(
                base, snippet, base_sizes
            )

    for base_name in base_names:
        row = [base_name]
        for snippet_name in snippet_names:
            self_size = taught_sizes[snippet_name][snippet_name]
            logging.debug(
                "%s  %s %s %s",
                base_name,
                snippet_name,
                taught_sizes[base_name][snippet_name],
                self_size,
            )
            row.append(str(self_size - taught_sizes[base_name][snippet_name]))
        print(",".join(row))


if __name__ == "__main__":
    main()
