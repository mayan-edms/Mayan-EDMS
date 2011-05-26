from django import forms

from common.forms import DetailForm

from history.models import History


class HistoryDetailForm(DetailForm):
    class Meta:
        model = History
        exclude = ('datetime', 'content_type', 'object_id', 'history_type', 'dictionary')
