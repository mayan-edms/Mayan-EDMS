# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

DEFAULT_ZOOM_LEVEL = 100
DEFAULT_ROTATION = 0
DEFAULT_PAGE_NUMBER = 1
DEFAULT_FILE_FORMAT = 'jpeg'
DEFAULT_FILE_FORMAT_MIMETYPE = 'image/jpeg'

DIMENSION_SEPARATOR = 'x'

TRANSFORMATION_RESIZE = 'resize'
TRANSFORMATION_ROTATE = 'rotate'
TRANSFORMATION_DENSITY = 'density'
TRANSFORMATION_ZOOM = 'zoom'

TRANSFORMATION_CHOICES = {
    TRANSFORMATION_RESIZE: {
        'label': _('Resize'),
        'description': _('Resize.'),
        'arguments': [
            {'name': 'width', 'label': _('Width'), 'required': True},
            {'name': 'height', 'label': _('Height'), 'required': False},
        ]
    },
    TRANSFORMATION_ROTATE: {
        'label': _('Rotate'),
        'description': _('Rotate by n degress.'),
        'arguments': [
            {'name': 'degrees', 'label': _('Degrees'), 'required': True}
        ]
    },
    TRANSFORMATION_DENSITY: {
        'label': _('Density'),
        'description': _('Change the resolution (ie: DPI) without resizing.'),
        'arguments': [
            {'name': 'width', 'label': _('Width'), 'required': True},
            {'name': 'height', 'label': _('Height'), 'required': False},
        ]
    },
    TRANSFORMATION_ZOOM: {
        'label': _('Zoom'),
        'description': _('Zoom by n percent.'),
        'arguments': [
            {'name': 'percent', 'label': _('Percent'), 'required': True}
        ]
    },
}
