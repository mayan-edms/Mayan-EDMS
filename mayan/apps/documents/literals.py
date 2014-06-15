from django.utils.translation import ugettext_lazy as _

PICTURE_ERROR_SMALL = u'picture_error.png'
PICTURE_ERROR_MEDIUM = u'1297211435_error.png'
PICTURE_UNKNOWN_SMALL = u'1299549572_unknown2.png'
PICTURE_UNKNOWN_MEDIUM = u'1299549805_unknown.png'

RELEASE_LEVEL_FINAL = 1
RELEASE_LEVEL_ALPHA = 2
RELEASE_LEVEL_BETA = 3
RELEASE_LEVEL_RC = 4
RELEASE_LEVEL_HF = 5

RELEASE_LEVEL_CHOICES = (
    (RELEASE_LEVEL_FINAL, _(u'final')),
    (RELEASE_LEVEL_ALPHA, _(u'alpha')),
    (RELEASE_LEVEL_BETA, _(u'beta')),
    (RELEASE_LEVEL_RC, _(u'release candidate')),
    (RELEASE_LEVEL_HF, _(u'hotfix')),
)

VERSION_UPDATE_MAJOR = u'major'
VERSION_UPDATE_MINOR = u'minor'
VERSION_UPDATE_MICRO = u'micro'

DEFAULT_ZIP_FILENAME = u'document_bundle.zip'
