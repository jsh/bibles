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

    >>> os.chdir('/var/tmp')
    >>> open('sizetest', "w+").close()
    >>> x = Sizes('/var/tmp')
    >>> x.size('sizetest')
    8

    >>> os.unlink('/var/tmp/sizetest')
    >>> x = Sizes('/var/tmp')
    >>> x.size('sizetest')

    """

    def __init__(self, directory="."):
        def file_sizes(directory):
            size_file = os.path.join(directory, ".sizes.json")
            try:
                with open(size_file, "r") as stream:
                    sizes = json.load(stream)
            except Exception:
                sizes = {}
            filenames = os.listdir(directory)
            # remove the ones that are gone
            sizes = {
                filename: size
                for filename, size in sizes.items()
                if filename in filenames
            }

            # add anything missing
            for filename in filenames:
                file_path = os.path.join(directory, filename)
                if (  # pylint: disable=C0330
                    os.path.isfile(file_path)
                    and not_json(file_path)
                    and filename not in sizes
                ):
                    sizes[filename] = compressed_size(file_path)
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

    def size(self, filename):
        """Compressed size of file."""
        try:
            return self._sizes[filename]
        except KeyError:
            pass
