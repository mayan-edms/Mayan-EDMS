from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_content_type_kwargs_factory

from .icons import (
    icon_about, icon_book, icon_documentation, icon_forum, icon_license,
    icon_object_copy, icon_setup, icon_source_code, icon_store, icon_support,
    icon_tools
)


def object_copy_conditional_disable(context):
    from .classes import ModelCopy

    try:
        resolved_object = context['resolved_object']
    except KeyError:
        return False
    else:
        try:
            return ModelCopy.get(
                model=resolved_object._meta.model
            ).test_condition(instance=resolved_object)
        except KeyError:
            return False


link_about = Link(
    icon=icon_about, text=_('About this'), view='common:about_view'
)
link_book = Link(
    icon=icon_book, tags='new_window', text=_('Get the book'),
    url='https://mayan-edms.com/book/'
)
link_documentation = Link(
    icon=icon_documentation, tags='new_window',
    text=_('Documentation'), url='https://docs.mayan-edms.com'
)
link_forum = Link(
    icon=icon_forum, tags='new_window', text=_('Forum'),
    url='https://forum.mayan-edms.com'
)
link_license = Link(
    icon=icon_license, text=_('License'), view='common:license_view'
)
link_object_copy = Link(
    condition=object_copy_conditional_disable,
    icon=icon_object_copy, kwargs=get_content_type_kwargs_factory(),
    text=_('Copy'), view='common:object_copy'
)
link_setup = Link(
    icon=icon_setup, text=_('Setup'), view='common:setup_list'
)
link_source_code = Link(
    icon=icon_source_code, tags='new_window', text=_('Source code'),
    url='https://gitlab.com/mayan-edms/mayan-edms'
)
link_store = Link(
    icon=icon_store, tags='new_window', text=_('Online store'),
    url='https://teespring.com/stores/mayan-edms'
)
link_support = Link(
    icon=icon_support, tags='new_window', text=_('Get support'),
    url='http://www.mayan-edms.com/providers/'
)
link_tools = Link(
    icon=icon_tools, text=_('Tools'), view='common:tools_list'
)
