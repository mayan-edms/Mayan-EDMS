from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_document_verify

label = _(u'Document signatures')
description = _(u'Handles document signatures.')
dependencies = ['app_registry', 'icons', 'navigation', 'django_gpg', 'documents', 'permissions']
icon = icon_document_verify
