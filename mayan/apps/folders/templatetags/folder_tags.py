from django.core.urlresolvers import reverse
from django.template import Library

from django.utils.translation import ugettext as _

from folders.forms import AddDocumentForm

register = Library()


@register.inclusion_tag('generic_form_subtemplate.html', takes_context=True)
def get_add_document_to_folder_form(context):
    context.update({
        'form': AddDocumentForm(user=context['request'].user),
        'request': context['request'],
        'form_action': reverse('folder_add_document_sidebar', args=[context['object'].pk]),
        'title': _('Add document to a folder')
    })
    return context
