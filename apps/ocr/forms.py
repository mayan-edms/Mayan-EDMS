from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DetailForm

from models import DocumentQueue


class DocumentQueueForm_view(DetailForm):
    class Meta:
        model = DocumentQueue
        exclude = ('name', 'label')

    def __init__(self, *args, **kwargs):
        super(DocumentQueueForm_view, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['class'] = 'undecorated_list'   
