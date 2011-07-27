from django.utils.translation import ugettext_lazy as _

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

SOURCE_ICON_CHOICES = (
    (SOURCE_ICON_DISK, _(u'Disk')),
    (SOURCE_ICON_DATABASE, _(u'Database')),
    (SOURCE_ICON_DRIVE, _(u'Drive')),
    (SOURCE_ICON_DRIVE_NETWORK, _(u'Network drive')),
    (SOURCE_ICON_DRIVE_USER, _(u'User drive')),
    (SOURCE_ICON_EMAIL, _(u'Envelope')),
    (SOURCE_ICON_FOLDER, _(u'Folder')),
    (SOURCE_ICON_WORLD, _(u'World')),
    (SOURCE_ICON_PRINTER, _(u'Printer')),
    (SOURCE_ICON_PRINTER_EMPTY, _(u'Empty printer')),
)

SOURCE_CHOICE_WEB_FORM = 'webform'
SOURCE_CHOICE_STAGING = 'staging'
SOURCE_CHOICE_WATCH = 'watch'

SOURCE_CHOICES = (
    (SOURCE_CHOICE_WEB_FORM, _(u'web form')),
    (SOURCE_CHOICE_STAGING, _(u'server staging folder')),
    (SOURCE_CHOICE_WATCH, _(u'server watch folder')),
)

SOURCE_CHOICES_PLURAL = (
    (SOURCE_CHOICE_WEB_FORM, _(u'web forms')),
    (SOURCE_CHOICE_STAGING, _(u'server staging folders')),
    (SOURCE_CHOICE_WATCH, _(u'server watch folders')),
)
