from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import PERMISSION_HISTORY_VIEW

history_list = {'text': _(u'history'), 'view': 'history_list', 'famfam': 'book', 'icon': 'book.png', 'children_view_regex': [r'history_[l,v]']}
history_details = {'text': _(u'details'), 'view': 'history_view', 'famfam': 'book_open', 'args': 'object.pk', 'permissions': [PERMISSION_HISTORY_VIEW]}
