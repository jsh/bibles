#!/usr/bin/env python3

'''Parse the args'''

import argparse


def parseargs():
    '''Parse arguments.'''
    parser = argparse.ArgumentParser(description='Show compression gains.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Turn on debugging'
                       )
    return parser.parse_args()

if __name__ == '__main__':
    print(parseargs().debug)
