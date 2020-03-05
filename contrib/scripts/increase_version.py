#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import sys

import version


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(
            'usage: <part to increase [major, minor, micro]> <-test>'
        )
        exit(0)

    if len(sys.argv) < 3:
        print('Insufficient arguments')
        exit(1)

    version_string = sys.argv[1]
    if version_string == '-':
        version_string = sys.stdin.read().replace('\n', '')

    version = version.Version(version_string=version_string)
    part = sys.argv[2].lower()

    if part == 'major':
        version.increment_major()
    elif part == 'minor':
        version.increment_minor()
    elif part == 'micro':
        version.increment_micro()
    else:
        print('Unknown part')
        exit(1)

    print(version.get_version_string())
