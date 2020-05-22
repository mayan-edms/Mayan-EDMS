import platform

if platform.system() in ('FreeBSD', 'OpenBSD', 'Darwin'):
    DEFAULT_PDFTOTEXT_PATH = '/usr/local/bin/pdftotext'
else:
    DEFAULT_PDFTOTEXT_PATH = '/usr/bin/pdftotext'
