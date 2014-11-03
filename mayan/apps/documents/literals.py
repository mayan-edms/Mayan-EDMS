import pycountry

PICTURE_ERROR_SMALL = u'picture_error.png'
PICTURE_ERROR_MEDIUM = u'1297211435_error.png'
PICTURE_UNKNOWN_SMALL = u'1299549572_unknown2.png'
PICTURE_UNKNOWN_MEDIUM = u'1299549805_unknown.png'

VERSION_UPDATE_MAJOR = u'major'
VERSION_UPDATE_MINOR = u'minor'
VERSION_UPDATE_MICRO = u'micro'

DEFAULT_ZIP_FILENAME = u'document_bundle.zip'

LANGUAGE_CHOICES = [(i.bibliographic, i.name) for i in list(pycountry.languages)]
