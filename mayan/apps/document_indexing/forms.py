from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.classes import ModelProperty
from mayan.apps.common.forms import FilteredSelectionForm
from mayan.apps.documents.models import Document

from .models import Index, IndexTemplateNode
from .permissions import permission_document_indexing_rebuild


class DocumentTemplateSandboxForm(forms.Form):
    template = forms.CharField(
        help_text=_(
            'The template string to be evaluated. The current document '
            'is available as the {{ document }} variable.'
        ), label=_('Template'), widget=forms.widgets.Textarea(
            attrs={'rows': 5}
        )
    )
    result = forms.CharField(
        help_text=_('Resulting text from the evaluated template.'),
        label=_('Result'), required=False, widget=forms.widgets.Textarea(
            attrs={'rows': 5}
        )
    )

    def __init__(self, *args, **kwargs):
        super(DocumentTemplateSandboxForm, self).__init__(*args, **kwargs)
        self.fields['template'].help_text = ' '.join(
            [
                force_text(self.fields['template'].help_text),
                force_text(
                    _(
                        'Use Django\'s default templating language '
                        '(https://docs.djangoproject.com/en/1.11/ref/templates/builtins/)'
                    ),
                ),
                '<br>',
                ModelProperty.get_help_text_for(
                    model=Document, show_name=True
                ).replace('\n', '<br>')
            ]
        )


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
