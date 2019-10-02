#!/usr/bin/env python
"""How much can snippet compression learn from different bases?"""

import os
import zlib

import parseargs
import sizes
from sizes import Sizes

# pylint: disable=line-too-long


def teaching_gain(base, snippet, base_size, snippet_size, combined_size):
    """Gain in compression through teaching.

    Scaled to make the numbers easy to read.
    """
    taught_snippet_size = combined_size - base_size[base]
    return (1 - (taught_snippet_size) / snippet_size[snippet]) * 1000


def main():
    """The feature attraction."""
    args = parseargs.parseargs()

    base_dir = "ot"
    snippet_dir = "nt"
    bases = [file for file in os.listdir(base_dir) if sizes.not_json(file)]
    snippets = [file for file in os.listdir(snippet_dir) if sizes.not_json(file)]
    base_size = Sizes(base_dir).sizes()
    snippet_size = Sizes(snippet_dir).sizes()
    for base in bases:
        print(base)
        with open(os.path.join(base_dir, base), "rb") as bfd:
            base_text = bfd.read()
            for snippet in snippets:
                with open(os.path.join(snippet_dir, snippet), "rb") as sfd:
                    snippet_text = sfd.read()
                    combined_size = len(zlib.compress(base_text + snippet_text))
                    gain = teaching_gain(
                        base, snippet, base_size, snippet_size, combined_size
                    )
                    if args.debug:
                        fmt = (
                            "base_size[{}] = {}, "
                            "snippet_size[{}] = {}, "
                            "combined_size = {}, "
                            "teaching_gain = {}"
                        )

                        print(
                            fmt.format(
                                base,
                                base_size[base],
                                snippet,
                                snippet_size[snippet],
                                combined_size,
                                gain,
                            )
                        )


if __name__ == "__main__":
    main()
