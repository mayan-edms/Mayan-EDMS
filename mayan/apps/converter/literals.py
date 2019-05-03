from __future__ import unicode_literals

import platform

if platform.system() == 'OpenBSD':
    DEFAULT_LIBREOFFICE_PATH = '/usr/local/bin/libreoffice'
    DEFAULT_PDFINFO_PATH = '/usr/local/bin/pdfinfo'
    DEFAULT_PDFTOPPM_PATH = '/usr/local/bin/pdftoppm'
else:
    DEFAULT_LIBREOFFICE_PATH = '/usr/bin/libreoffice'
    DEFAULT_PDFINFO_PATH = '/usr/bin/pdfinfo'
    DEFAULT_PDFTOPPM_PATH = '/usr/bin/pdftoppm'

DEFAULT_ZOOM_LEVEL = 100
DEFAULT_ROTATION = 0
DEFAULT_PAGE_NUMBER = 1
DEFAULT_PILLOW_FORMAT = 'JPEG'

DEFAULT_PDFTOPPM_DPI = 300
DEFAULT_PDFTOPPM_FORMAT = 'jpeg'  # Possible values jpeg, png, tiff
