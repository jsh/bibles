#!/usr/bin/env python
"""Sizes module."""

import json
import os
import zlib


def compressed_size(filename):
    """Compressed file size.

    >>> compressed_size('/dev/null')
    8
    """
    with open(filename, "rb") as stream:
        text = stream.read()
        return len(zlib.compress(text))


def not_json(filename):
    """True iff the file's NOT json.

    >>> not_json('foo')
    True
    >>> not_json('foo.json')
    False
    """
    return filename[-5:] != ".json"


class Sizes:
    """Encapsulate information about compressed file sizes in directory.

    >>> Sizes() #doctest: +ELLIPSIS
    sizes.Sizes('.')
    """

    def __init__(self, directory="."):
        def file_sizes(directory):
            size_file = os.path.join(directory, ".sizes.json")
            try:
                with open(size_file, "r") as stream:
                    sizes = json.load(stream)
            except Exception:
                sizes = {}
            files = os.listdir(directory)
            # remove the ones that are gone
            sizes = {file: size for file, size in sizes.items() if file in files}

            # add anything missing
            for file in files:
                if os.path.isfile(file) and not_json(file) and file not in sizes:
                    sizes[file] = compressed_size(os.path.join(directory, file))
            with open(size_file, "w") as stream:
                json.dump(sizes, stream)
            return sizes

        self._directory = directory
        self._sizes = file_sizes(directory)

    def __repr__(self):
        return "{}.{}('{}')".format(
            self.__class__.__module__, self.__class__.__qualname__, self._directory
        )

    def sizes(self):
        """All sizes."""
        return self._sizes

    def size(self, file):
        """Compressed size of file."""
        return self._sizes[file]
