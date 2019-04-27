from __future__ import unicode_literals

from .transformations import (  # NOQA
    BaseTransformation, TransformationResize, TransformationRotate,
    TransformationZoom
)

default_app_config = 'mayan.apps.converter.apps.ConverterApp'
