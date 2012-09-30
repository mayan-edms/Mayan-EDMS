from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from icons.literals import (DISK, DATABASE, DRIVE, DRIVE_NETWORK, DRIVE_USER,
    EMAIL, FOLDER, WORLD, PRINTER, PRINTER_EMPTY, IMAGES)

POP3_PORT = 110
POP3_SSL_PORT = 995
DEFAULT_POP3_INTERVAL = 15 * 60 # 15 minutes in seconds

IMAP_PORT = 143
IMAP_SSL_PORT = 993
DEFAULT_IMAP_INTERVAL = 15 * 60 # 15 minutes in seconds
IMAP_LOCK_TIMEOUT = 60
IMAP_DEFAULT_MAILBOX = 'INBOX'

SOURCE_UNCOMPRESS_CHOICE_Y = 'y'
SOURCE_UNCOMPRESS_CHOICE_N = 'n'
SOURCE_UNCOMPRESS_CHOICE_ASK = 'a'

SOURCE_UNCOMPRESS_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_Y, _(u'Always')),
    (SOURCE_UNCOMPRESS_CHOICE_N, _(u'Never')),
)

SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_Y, _(u'Always')),
    (SOURCE_UNCOMPRESS_CHOICE_N, _(u'Never')),
    (SOURCE_UNCOMPRESS_CHOICE_ASK, _(u'Ask user'))
)

SOURCE_ICON_CHOICES = (
    (DISK, _(u'Disk')),
    (DATABASE, _(u'Database')),
    (DRIVE, _(u'Drive')),
    (DRIVE_NETWORK, _(u'Network drive')),
    (DRIVE_USER, _(u'User drive')),
    (EMAIL, _(u'Envelope')),
    (FOLDER, _(u'Folder')),
    (IMAGES, _(u'Images')),
    (WORLD, _(u'World')),
    (PRINTER, _(u'Printer')),
    (PRINTER_EMPTY, _(u'Empty printer')),
)

SOURCE_CHOICE_WEB_FORM = 'webform'
SOURCE_CHOICE_STAGING = 'staging'
SOURCE_CHOICE_WATCH = 'watch'
SOURCE_CHOICE_POP3_EMAIL = 'pop3'
SOURCE_CHOICE_IMAP_EMAIL = 'imap'
SOURCE_CHOICE_LOCAL_SCANNER = 'local_scanner'

SOURCE_CHOICES = (
    (SOURCE_CHOICE_WEB_FORM, _(u'web form')),
    (SOURCE_CHOICE_STAGING, _(u'server staging folder')),
    (SOURCE_CHOICE_WATCH, _(u'server watch folder')),
    (SOURCE_CHOICE_POP3_EMAIL, _(u'POP3 email')),
    (SOURCE_CHOICE_IMAP_EMAIL, _(u'IMAP email')),
    (SOURCE_CHOICE_LOCAL_SCANNER, _(u'local scanner')),
)

SOURCE_CHOICES_PLURAL = (
    (SOURCE_CHOICE_WEB_FORM, _(u'web forms')),
    (SOURCE_CHOICE_STAGING, _(u'server staging folders')),
    (SOURCE_CHOICE_WATCH, _(u'server watch folders')),
    (SOURCE_CHOICE_POP3_EMAIL, _(u'POP3 emails')),
    (SOURCE_CHOICE_IMAP_EMAIL, _(u'IMAP emails')),
    (SOURCE_CHOICE_LOCAL_SCANNER, _(u'local scanners')),
)

DEFAULT_LOCAL_SCANNER_FILE_FORMAT = 'JPEG'
DEFAULT_POP3_DEFAULT_TIMEOUT = 10  # for POP3 only not POP3_SSL
DEFAULT_EMAIL_PROCESSING_INTERVAL = 60
DEFAULT_POP3_EMAIL_LOG_COUNT = 10  # Max log entries to store
