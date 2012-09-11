from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_file_extension_unknown

label = _(u'MIME types')
description = _(u'Handles the MIME type detection.')
icon = icon_file_extension_unknown
dependencies = ['app_registry', 'icons']
