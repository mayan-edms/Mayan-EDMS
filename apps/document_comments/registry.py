from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_comments_for_document

label = _(u'Comments')
description = _(u'Handles document comments.')
icon = icon_comments_for_document
dependencies = ['app_registry', 'icons', 'documents', 'permissions', 'navigation']
