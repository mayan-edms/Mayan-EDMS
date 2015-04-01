from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.translation import ugettext_lazy as _

from ..forms import SearchForm
from ..models import RecentSearch
from ..settings import RECENT_COUNT

register = Library()


@register.inclusion_tag('appearance/generic_subtemplate.html', takes_context=True)
def recent_searches_template(context):
    if not context['user'].is_anonymous():
        recent_searches = RecentSearch.objects.filter(user=context['user'])
    else:
        return context

    context.update({
        'request': context['request'],
        'side_bar': True,
        'title': _('Recent searches (maximum of %d)') % RECENT_COUNT,
        'paragraphs': [
            '<a href="%(url)s"><span class="famfam active famfam-%(icon)s"></span>%(text)s</a>' % {
                'text': rs,
                'url': rs.url(),
                'icon': 'zoom_in' if rs.is_advanced() else 'zoom',
            } for rs in recent_searches
        ]
    })
    return context
