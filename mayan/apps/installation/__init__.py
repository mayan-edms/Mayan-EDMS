from __future__ import unicode_literals

from django.db.utils import DatabaseError
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from south.signals import post_migrate

from common.utils import encapsulate
from navigation.api import register_links, register_model_list_columns
from project_tools.api import register_tool

from .classes import Property, PropertyNamespace
from .links import link_menu_link, link_namespace_details, link_namespace_list
from .models import Installation


@receiver(post_migrate, dispatch_uid='create_installation_instance')
def create_installation_instance(sender, **kwargs):
    if kwargs['app'] == 'installation':
        Installation.objects.get_or_create()


register_model_list_columns(PropertyNamespace, [
    {
        'name': _('Label'),
        'attribute': 'label'
    },
    {
        'name': _('Items'),
        'attribute': encapsulate(lambda entry: len(entry.get_properties()))
    }
])

register_model_list_columns(Property, [
    {
        'name': _('Label'),
        'attribute': 'label'
    },
    {
        'name': _('Value'),
        'attribute': 'value'
    }
])

register_links(PropertyNamespace, [link_namespace_details])
register_links(['installation:namespace_list', PropertyNamespace], [link_namespace_list], menu_name='secondary_menu')
register_tool(link_menu_link)
