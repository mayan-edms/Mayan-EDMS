import platform

if platform.system() in ('FreeBSD', 'OpenBSD', 'Darwin'):
    DEFAULT_EXIF_PATH = '/usr/local/bin/exiftool'
else:
    DEFAULT_EXIF_PATH = '/usr/bin/exiftool'

LOCK_EXPIRE = 60 * 10  # Adjust to worst case scenario

DEFAULT_FILE_METADATA_AUTO_PROCESS = True
DEFAULT_FILE_METADATA_DRIVERS_ARGUMENTS = {
    'exif_driver': {'exiftool_path': DEFAULT_EXIF_PATH}
}
