from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import FilteredSelectionForm

from .widgets import TagFormWidget


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
