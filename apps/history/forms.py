from __future__ import absolute_import

from common.forms import DetailForm

from .models import History


class HistoryDetailForm(DetailForm):
    class Meta:
        model = History
        exclude = ('datetime', 'content_type', 'object_id', 'history_type', 'dictionary')
