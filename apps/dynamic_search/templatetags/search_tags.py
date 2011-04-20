from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.translation import ugettext as _

from dynamic_search.forms import SearchForm

register = Library()


@register.inclusion_tag('search_results_subtemplate.html', takes_context=True)
def search_form(context):
    context.update({
        'form': SearchForm(initial={'q': context.get('query_string', '')}),
        'request': context['request'],
        'MEDIA_URL': context['MEDIA_URL'],
        'form_action': reverse('results'),
        'form_title': _(u'Search')
    })
    return context
