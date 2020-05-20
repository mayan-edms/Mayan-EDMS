from django import forms

from mayan.apps.common.forms import DetailForm

from .models import Comment


class DocumentCommentDetailForm(DetailForm):

    class Meta:
        fields = ('comment',)
        extra_fields = (
            {'field': 'submit_date', 'widget': forms.widgets.DateTimeInput},
            {'field': 'user'},
        )
        model = Comment
