import platform

if platform.system() in ('FreeBSD', 'OpenBSD', 'Darwin'):
    DEFAULT_DOCUMENT_PARSING_PDFTOTEXT_PATH = '/usr/local/bin/pdftotext'
else:
    DEFAULT_DOCUMENT_PARSING_PDFTOTEXT_PATH = '/usr/bin/pdftotext'

DEFAULT_DOCUMENT_PARSING_AUTO_PARSING = True
