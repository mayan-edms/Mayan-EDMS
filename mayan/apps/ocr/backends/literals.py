from __future__ import absolute_import, unicode_literals

import platform

if platform.system() in ('FreeBSD', 'OpenBSD', 'Darwin'):
    DEFAULT_TESSERACT_BINARY_PATH = '/usr/local/bin/tesseract'
else:
    DEFAULT_TESSERACT_BINARY_PATH = '/usr/bin/tesseract'

DEFAULT_TESSERACT_TIMEOUT = 600  # 600 seconds, 10 minutes
