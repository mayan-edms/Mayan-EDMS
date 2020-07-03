from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Search'), name='search')

event_search_advanced = namespace.add_event_type(
    extra_data_template_name='dynamic_search/events/search_advanced.html',
    label=_('Advanced search'), name='search_advanced'
)
event_search_simple = namespace.add_event_type(
    extra_data_template_name='dynamic_search/events/search_simple.html',
    label=_('Simple search'), name='search_simple'
)
