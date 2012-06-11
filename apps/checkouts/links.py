from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from documents.permissions import PERMISSION_DOCUMENT_VIEW

from .permissions import (PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN)

checkout_list = {'text': _(u'check in/out'), 'view': 'checkout_list', 'famfam': 'basket'}
checkout_document = {'text': _('check out document'), 'view': 'checkout_document', 'args': 'object.pk', 'famfam': 'basket_put'}#, 'permissions': [PERMISSION_DOCUMENT_CHECKOUT]}
checkin_document = {'text': _('check out document'), 'view': 'checkout_document', 'args': 'object.pk', 'famfam': 'basket_remove'}#, 'permissions': [PERMISSION_DOCUMENT_CHECKIN]}
checkout_info = {'text': _('check in/out'), 'view': 'checkout_info', 'args': 'object.pk', 'famfam': 'basket', 'children_views': ['checkout_document', 'checkin_document']}#, 'permissions': [PERMISSION_DOCUMENT_CHECKIN]}
