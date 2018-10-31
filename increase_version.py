#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import doctest
import re
import sys

import mayan


VERSION_PART_MAJOR = 0
VERSION_PART_MINOR = 1
VERSION_PART_MICRO = 2


class Version(object):
    """
    >>> Version('1')
    Version: 1
    >>> Version('1.0')
    Version: 1.0
    >>> Version('1.3.2')
    Version: 1.3.2
    >>> Version('1').increment_part(part=VERSION_PART_MAJOR)
    Version: 2
    >>> Version('1').increment_part(part=VERSION_PART_MINOR)
    Version: 1.1
    >>> Version('1').increment_part(part=VERSION_PART_MICRO)
    Version: 1.0.1
    >>> Version('1rc').increment_part(part=VERSION_PART_MAJOR)
    Version: 2rc
    >>> Version('1rc2').increment_part(part=VERSION_PART_MAJOR)
    Version: 1rc3
    >>> Version('1rc0').increment_part(part=VERSION_PART_MAJOR)
    Version: 1rc1
    >>> Version('1.rc0').increment_part(part=VERSION_PART_MINOR)
    Version: 1.rc1
    >>> Version('1.0.rc1').increment_part(part=VERSION_PART_MINOR)
    Version: 1.1
    >>> Version('1.0.rc1').increment_part(part=VERSION_PART_MICRO)
    Version: 1.0.rc2
    >>> Version('1rc').increment_part(part=VERSION_PART_MINOR)
    Version: 1rc.1
    >>> Version('1rc').increment_part(part=VERSION_PART_MINOR)
    Version: 1rc.1
    >>> Version('1rc').increment_part(part=VERSION_PART_MICRO)
    Version: 1rc.0.1
    >>> Version('1.rc1').increment_part(part=VERSION_PART_MINOR)
    Version: 1.rc2
    >>> Version('1.rc1').increment_part(part=VERSION_PART_MICRO)
    Version: 1.rc1.1
    >>> Version('1.1.rc1').increment_part(part=VERSION_PART_MICRO)
    Version: 1.1.rc2
    >>> Version('1.2.3').increment_major()
    Version: 2
    >>> Version('1.2.3').increment_minor()
    Version: 1.3
    >>> Version('1.2.3').increment_micro()
    Version: 1.2.4
    """
    def __init__(self, version_string):
        self._version_string = version_string
        self._version_parts = version_string.split('.')

    def _get_version_part(self, index):
        try:
            return self._version_parts[index]
        except IndexError:
            return 0

    def __repr__(self):
        return 'Version: {}'.format(self.get_version_string())

    def increment_major(self):
        return self.increment_part(part=VERSION_PART_MAJOR)

    def increment_minor(self):
        return self.increment_part(part=VERSION_PART_MINOR)

    def increment_micro(self):
        return self.increment_part(part=VERSION_PART_MICRO)

    def increment_part(self, part):
        # Fill version parts if the requested part is lower than what is
        # available
        self._version_parts.extend(
            ['0'] * (part - len(self._version_parts) + 1)
        )

        try:
            version_part = self._version_parts[part]
        except IndexError:
            part_numeric_post = ''
            part_numeric_pre = ''
            part_text = ''
        else:
            part_numeric_pre, part_text, part_numeric_post = re.findall(
                '^(\d+)*([A-Za-z]+)*(\d+)*$', version_part
            )[0]

        if part_numeric_post:
            part_numeric_post = int(part_numeric_post) + 1
        else:
            part_numeric_pre = int(part_numeric_pre) + 1

        self._version_parts[part] = '{}{}{}'.format(
            part_numeric_pre, part_text, part_numeric_post
        )

        # Discard version parts lower than what is being increased
        self._version_parts = self._version_parts[0:part + 1]
        self._version_string = '.'.join(self._version_parts)

        return self

    def get_version_string(self):
        return self._version_string

    @property
    def major(self):
        return self._get_version_part(VERSION_PART_MAJOR)

    @property
    def minor(self):
        return self._get_version_part(VERSION_PART_MINOR)

    @property
    def micro(self):
        return self._get_version_part(VERSION_PART_MICRO)


if __name__ == '__main__':
    # Remove comment to run tests
    # doctest.testmod()
    # exit(0)

    if len(sys.argv) == 1:
        print(
            'usage: <part to increase [major, minor, micro]>'
        )
        exit(0)

    if len(sys.argv) < 3:
        print('Insufficient arguments')
        exit(1)

    version_string = sys.argv[1]
    if version_string == '-':
        version_string = sys.stdin.read().replace('\n', '')

    version = Version(version_string)
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
