#!/usr/bin/env python3

"""Parse the args"""

import argparse
import logging

BASE_DIR = "ot.d"
SNIPPET_DIR = "nt.d"


def parseargs():
    """Parse arguments."""
    parser = argparse.ArgumentParser(description="Show compression gains.")
    parser.add_argument("--debug", action="store_true", help="Turn on debugging")
    parser.add_argument(
        "--base_dir", default=BASE_DIR, help="directory of training bases"
    )
    parser.add_argument(
        "--snippet_dir", default=SNIPPET_DIR, help="directory of snippets to compress"
    )
    args = parser.parse_args()

    # turn on logging
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))
    logging.debug("base_dir: %s", args.base_dir)
    logging.debug("snippet_dir: %s", args.snippet_dir)

    return args


if __name__ == "__main__":
    print(parseargs().debug)
