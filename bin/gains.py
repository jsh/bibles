#!/usr/bin/env python
"""How much can snippet compression learn from different bases?"""

import os
import zlib

import parseargs
import sizes
from sizes import Sizes

debug = False


def teaching_gain(base, snippet, base_size, snippet_size, combined_size):
    """Gain in compression through teaching.

    Scaled to make the numbers easy to read.
    """
    taught_snippet_size = combined_size - base_size[base]
    teaching_gain = (1 - (taught_snippet_size) / snippet_size[snippet]) * 1000
    if debug:
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
                teaching_gain,
            )
        )

    return teaching_gain


def main():
    """The feature attraction."""
    global debug
    debug = parseargs.parseargs().debug

    base_dir = "ot"
    snippet_dir = "nt"
    bases = [file for file in os.listdir(base_dir) if sizes.not_json(file)]
    snippets = [file for file in os.listdir(snippet_dir) if sizes.not_json(file)]
    base_size = Sizes(base_dir).sizes()
    snippet_size = Sizes(snippet_dir).sizes()
    column_headers = [""] + snippets
    print(",".join(column_headers))

    for base in bases:
        line = [base]
        with open(os.path.join(base_dir, base), "rb") as bfd:
            base_text = bfd.read()
            for snippet in snippets:
                with open(os.path.join(snippet_dir, snippet), "rb") as sfd:
                    snippet_text = sfd.read()
                    combined_size = len(zlib.compress(base_text + snippet_text))
                    gain = teaching_gain(
                        base, snippet, base_size, snippet_size, combined_size
                    )
                    line.append(str(round(gain)))

            print(",".join(line))


if __name__ == "__main__":
    main()
