from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.classes import ModelProperty
from documents.models import Document

from .models import Index, IndexTemplateNode
from .permissions import permission_document_indexing_rebuild


class IndexListForm(forms.Form):
    indexes = forms.ModelMultipleChoiceField(
        help_text=_('Indexes to be queued for rebuilding.'),
        label=_('Indexes'), queryset=Index.objects.none(),
        required=False, widget=forms.widgets.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(IndexListForm, self).__init__(*args, **kwargs)
        queryset = AccessControlList.objects.filter_by_access(
            permission=permission_document_indexing_rebuild, user=user,
            queryset=Index.objects.filter(enabled=True)
        )
        self.fields['indexes'].queryset = queryset


class IndexTemplateNodeForm(forms.ModelForm):
    """
    A standard model form to allow users to create a new index template node
    """
    def __init__(self, *args, **kwargs):
        super(IndexTemplateNodeForm, self).__init__(*args, **kwargs)
        self.fields['index'].widget = forms.widgets.HiddenInput()
        self.fields['parent'].widget = forms.widgets.HiddenInput()
        self.fields['expression'].help_text = ' '.join(
            [
                force_text(self.fields['expression'].help_text),
                '<br>',
                ModelProperty.get_help_text_for(
                    model=Document, show_name=True
                ).replace('\n', '<br>')
            ]
        )

    class Meta:
        fields = ('parent', 'index', 'expression', 'enabled', 'link_documents')
        model = IndexTemplateNode
