from __future__ import unicode_literals

import platform

if platform.system() in ('FreeBSD', 'OpenBSD', 'Darwin'):
    DEFAULT_EXIF_PATH = '/usr/local/bin/exiftool'
else:
    DEFAULT_EXIF_PATH = '/usr/bin/exiftool'

LOCK_EXPIRE = 60 * 10  # Adjust to worst case scenario
