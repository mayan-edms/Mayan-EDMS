from django.utils.translation import ugettext_lazy as _

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

SOURCE_ICON_DISK = 'disk'
SOURCE_ICON_DATABASE = 'database'
SOURCE_ICON_DRIVE = 'drive'
SOURCE_ICON_DRIVE_NETWORK = 'drive_network'
SOURCE_ICON_DRIVE_USER = 'drive_user'
SOURCE_ICON_EMAIL = 'email'
SOURCE_ICON_FOLDER = 'folder'
SOURCE_ICON_WORLD = 'world'
SOURCE_ICON_PRINTER = 'printer'
SOURCE_ICON_PRINTER_EMPTY = 'printer_empty'
SOURCE_ICON_IMAGES = 'images'

SOURCE_ICON_CHOICES = (
    (SOURCE_ICON_DISK, _(u'Disk')),
    (SOURCE_ICON_DATABASE, _(u'Database')),
    (SOURCE_ICON_DRIVE, _(u'Drive')),
    (SOURCE_ICON_DRIVE_NETWORK, _(u'Network drive')),
    (SOURCE_ICON_DRIVE_USER, _(u'User drive')),
    (SOURCE_ICON_EMAIL, _(u'Envelope')),
    (SOURCE_ICON_FOLDER, _(u'Folder')),
    (SOURCE_ICON_IMAGES, _(u'Images')),
    (SOURCE_ICON_WORLD, _(u'World')),
    (SOURCE_ICON_PRINTER, _(u'Printer')),
    (SOURCE_ICON_PRINTER_EMPTY, _(u'Empty printer')),
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
