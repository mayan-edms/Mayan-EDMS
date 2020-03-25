from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import FilteredSelectionForm
from mayan.apps.documents.models import Document
from mayan.apps.templating.fields import TemplateField

from .models import Index, IndexTemplateNode
from .permissions import permission_document_indexing_rebuild


class IndexTemplateFilteredForm(FilteredSelectionForm):
    class Meta:
        allow_multiple = True
        field_name = 'index_templates'
        help_text = _('Index templates to be queued for rebuilding.')
        label = _('Index templates')
        queryset = Index.objects.filter(enabled=True)
        permission = permission_document_indexing_rebuild
        widget_attributes = {'class': 'select2'}


class IndexTemplateNodeForm(forms.ModelForm):
    """
    A standard model form to allow users to create a new index template node
    """
    def __init__(self, *args, **kwargs):
        super(IndexTemplateNodeForm, self).__init__(*args, **kwargs)
        self.fields['index'].widget = forms.widgets.HiddenInput()
        self.fields['parent'].widget = forms.widgets.HiddenInput()
        self.fields['expression'] = TemplateField(
            label=_('Template'), model=Document,
            model_variable='document', required=False
        )

    class Meta:
        fields = ('parent', 'index', 'expression', 'enabled', 'link_documents')
        model = IndexTemplateNode
