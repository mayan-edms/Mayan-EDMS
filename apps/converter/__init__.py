import tempfile

from common.conf import settings as common_settings

TEMPORARY_DIRECTORY = common_settings.TEMPORARY_DIRECTORY if common_settings.TEMPORARY_DIRECTORY else tempfile.mkdtemp()

#ugettext = lambda s: s

#TRANFORMATION_ROTATE = (u'-rotate %(degrees)d', ugettext(u'Rotation, arguments: degrees'))
TRANFORMATION_CHOICES = {
    'rotate':'-rotate %(degrees)d'
}

#getattr(settings, 'CONVERTER_TRANSFORMATION_LIST', [
#    TRANFORMATION_ROTATE,
#    ])
