from django.utils.translation import ugettext_lazy as _

from converter.conf.settings import DEFAULT_OPTIONS
from converter.conf.settings import LOW_QUALITY_OPTIONS
from converter.conf.settings import HIGH_QUALITY_OPTIONS
from converter.conf.settings import PRINT_QUALITY_OPTIONS

DEFAULT_ZOOM_LEVEL = 100
DEFAULT_ROTATION = 0
DEFAULT_PAGE_NUMBER = 1
DEFAULT_FILE_FORMAT = u'jpeg'
DEFAULT_OCR_FILE_FORMAT = u'tif'

QUALITY_DEFAULT = u'quality_default'
QUALITY_LOW = u'quality_low'
QUALITY_HIGH = u'quality_high'
QUALITY_PRINT = u'quality_print'

QUALITY_SETTINGS = {
    QUALITY_DEFAULT: DEFAULT_OPTIONS,
    QUALITY_LOW: LOW_QUALITY_OPTIONS,
    QUALITY_HIGH: HIGH_QUALITY_OPTIONS,
    QUALITY_PRINT: PRINT_QUALITY_OPTIONS
}

DIMENSION_SEPARATOR = u'x'

TRANSFORMATION_RESIZE = u'resize'
TRANSFORMATION_ROTATE = u'rotate'
TRANSFORMATION_DENSITY = u'density'
TRANSFORMATION_ZOOM = u'zoom'

TRANSFORMATION_CHOICES = {
    TRANSFORMATION_RESIZE: {
        'label': _(u'Resize'),
        'description': _(u'Resize.'),
        'arguments': [
            {'name': 'width', 'label': _(u'width'), 'required': True},
            {'name': 'height', 'label': _(u'height'), 'required': False},
        ]
    },
    TRANSFORMATION_ROTATE: {
        'label': _(u'Rotate'),
        'description': _(u'Rotate by n degress.'),
        'arguments': [
            {'name': 'degrees', 'label': _(u'degrees'), 'required': True}
        ]
    },
    TRANSFORMATION_DENSITY: {
        'label': _(u'Density'),
        'description': _(u'Change the resolution (ie: DPI) without resizing.'),
        'arguments': [
            {'name': 'width', 'label': _(u'width'), 'required': True},
            {'name': 'height', 'label': _(u'height'), 'required': False},
        ]
    }, 
    TRANSFORMATION_ZOOM: {
        'label': _(u'Zoom'),
        'description': _(u'Zoom by n percent.'),
        'arguments': [
            {'name': 'percent', 'label': _(u'percent'), 'required': True}
        ]
    },        
}
