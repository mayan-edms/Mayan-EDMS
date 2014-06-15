from django.core.urlresolvers import reverse
from django.template import Library

from django.utils.translation import ugettext as _

from tags.forms import AddTagForm

register = Library()


@register.inclusion_tag('generic_form_subtemplate.html', takes_context=True)
def get_add_tag_to_document_form(context):
    context.update({
        'form': AddTagForm(),
        'request': context['request'],
        'form_action': reverse('tag_add_sidebar', args=[context['document'].pk]),
        'title': _('Add tag to document')
    })
    return context
