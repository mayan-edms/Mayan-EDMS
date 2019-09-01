from __future__ import unicode_literals

CONTROL_CODE_MAGIC_NUMBER = 'MCTRL1'
CONTROL_CODE_SEPARATOR = ':'

CONTROL_SHEET_CODE_IMAGE_CACHE_NAME = 'control_sheet_codes'
CONTROL_SHEET_CODE_IMAGE_CACHE_STORAGE_INSTANCE_PATH = 'mayan.apps.control_codes.storages.storage_controlsheetcodeimagecache'
CONTROL_SHEET_CODE_IMAGE_TASK_TIMEOUT = 60

DEFAULT_CONTROL_SHEET_CODE_IMAGE_CACHE_MAXIMUM_SIZE = 50 * 2 ** 20  # 50 Megabytes
