import os

import platform

from django.conf import settings

ASSET_IMAGE_TASK_TIMEOUT = 60  # seconds

CONVERTER_OFFICE_FILE_MIMETYPES = (
    'application/msword',
    'application/mswrite',
    'application/mspowerpoint',
    'application/msexcel',
    'application/pgp-keys',
    'application/vnd.ms-excel',
    'application/vnd.ms-excel.addin.macroEnabled.12',
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
    'application/vnd.ms-powerpoint',
    'application/vnd.oasis.opendocument.chart',
    'application/vnd.oasis.opendocument.chart-template',
    'application/vnd.oasis.opendocument.formula',
    'application/vnd.oasis.opendocument.formula-template',
    'application/vnd.oasis.opendocument.graphics',
    'application/vnd.oasis.opendocument.graphics-template',
    'application/vnd.oasis.opendocument.image',
    'application/vnd.oasis.opendocument.image-template',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.oasis.opendocument.presentation-template',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.presentationml.slide',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.oasis.opendocument.spreadsheet-template',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.text-master',
    'application/vnd.oasis.opendocument.text-template',
    'application/vnd.oasis.opendocument.text-web',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-office',
    'application/xml',
    'text/x-c',
    'text/x-c++',
    'text/x-pascal',
    'text/x-msdos-batch',
    'text/x-python',
    'text/x-shellscript',
    'text/plain',
    'text/rtf',
)

if platform.system() in ('FreeBSD', 'OpenBSD', 'Darwin'):
    DEFAULT_LIBREOFFICE_PATH = '/usr/local/bin/libreoffice'
    DEFAULT_PDFINFO_PATH = '/usr/local/bin/pdfinfo'
    DEFAULT_PDFTOPPM_PATH = '/usr/local/bin/pdftoppm'
else:
    DEFAULT_LIBREOFFICE_PATH = '/usr/bin/libreoffice'
    DEFAULT_PDFINFO_PATH = '/usr/bin/pdfinfo'
    DEFAULT_PDFTOPPM_PATH = '/usr/bin/pdftoppm'

DEFAULT_CONVERTER_ASSET_CACHE_MAXIMUM_SIZE = 10 * 2 ** 20  # 10 Megabytes
DEFAULT_CONVERTER_ASSET_CACHE_TIME = '31556926'
DEFAULT_CONVERTER_ASSET_CACHE_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_CONVERTER_ASSET_CACHE_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'converter_assets_cache')
}
DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'converter_assets')
}
DEFAULT_CONVERTER_GRAPHICS_BACKEND = 'mayan.apps.converter.backends.python.Python'
DEFAULT_PAGE_NUMBER = 1
DEFAULT_PDFTOPPM_DPI = 300
DEFAULT_PDFTOPPM_FORMAT = 'jpeg'  # Possible values jpeg, png, tiff
DEFAULT_PILLOW_FORMAT = 'JPEG'
DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS = 89478485  # Upstream default as of v6.2.1 (2019-01-16)
DEFAULT_ROTATION = 0
DEFAULT_ZOOM_LEVEL = 100

DEFAULT_CONVERTER_GRAPHICS_BACKEND_ARGUMENTS = {
    'libreoffice_path': DEFAULT_LIBREOFFICE_PATH,
    'pdftoppm_dpi': DEFAULT_PDFTOPPM_DPI,
    'pdftoppm_format': DEFAULT_PDFTOPPM_FORMAT,
    'pdftoppm_path': DEFAULT_PDFTOPPM_PATH,
    'pdfinfo_path': DEFAULT_PDFINFO_PATH,
    'pillow_format': DEFAULT_PILLOW_FORMAT,
    'pillow_maximum_image_pixels': DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS,
}

STORAGE_NAME_ASSETS = 'converter__assets'
STORAGE_NAME_ASSETS_CACHE = 'converter__assets_cache'

TASK_ASSET_IMAGE_GENERATE_RETRY_DELAY = 10
