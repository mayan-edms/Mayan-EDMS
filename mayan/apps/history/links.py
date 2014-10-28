from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import PERMISSION_HISTORY_VIEW

history_list = {'text': _(u'History'), 'view': 'history:history_list', 'famfam': 'book', 'icon': 'book.png'}
history_details = {'text': _(u'Details'), 'view': 'history:history_view', 'famfam': 'book_open', 'args': 'object.pk', 'permissions': [PERMISSION_HISTORY_VIEW]}
