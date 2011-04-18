from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import TemplateSyntaxError, Library, \
                            VariableDoesNotExist, Node, Variable
from django.utils.translation import ugettext as _

from dynamic_search.forms import SearchForm
from folders.forms import AddDocumentForm

register = Library()
   
   
@register.inclusion_tag('generic_form_subtemplate.html', takes_context=True)
def get_add_document_to_folder_form(context):
    context.update({
        'form': AddDocumentForm(user=context['request'].user),#, document=context['object']),
        #'form': SearchForm(initial={'q':context.get('query_string', '')}),
        'request': context['request'],
        #'MEDIA_URL': context['MEDIA_URL'],
        'form_action': reverse('folder_add_document' ,args=[context['object'].pk]),
        #'form_title': _(u'Search'),
        'title': _('Add document to a folder')
    })
    return context
