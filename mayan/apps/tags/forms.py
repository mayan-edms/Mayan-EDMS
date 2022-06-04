from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import FilteredSelectionForm
from mayan.apps.views.widgets import ColorWidget

from .models import Tag
from .widgets import TagFormWidget


class TagForm(forms.ModelForm):
    class Meta:
        fields = ('label', 'color')
        model = Tag
        widgets = {
            'color': ColorWidget()
        }


class TagMultipleSelectionForm(FilteredSelectionForm):
    class Media:
        js = ('tags/js/tags_form.js',)

    class Meta:
        allow_multiple = True
        field_name = 'tags'
        label = _('Tags')
        required = False
        widget_class = TagFormWidget
        widget_attributes = {'class': 'select2-tags'}
