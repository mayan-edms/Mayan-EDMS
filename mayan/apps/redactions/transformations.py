from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.transformations import (
    BaseTransformation, TransformationDrawRectanglePercent
)

from .layers import layer_redactions


class TransformationRedactionPercent(TransformationDrawRectanglePercent):
    arguments = ('left', 'top', 'right', 'bottom')
    label = _('Redaction')
    name = 'redaction_percent'
    template_name = 'redactions/cropper.html'


BaseTransformation.register(
    layer=layer_redactions, transformation=TransformationRedactionPercent
)
