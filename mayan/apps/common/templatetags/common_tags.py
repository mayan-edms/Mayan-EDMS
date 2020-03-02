from __future__ import unicode_literals

import logging

from django.template import Context, Library, Variable, VariableDoesNotExist
from django.template.defaultfilters import truncatechars
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.six import string_types
from django.utils.translation import ugettext_lazy as _

import mayan
from mayan.apps.appearance.settings import setting_max_title_length

from ..classes import MissingItem
from ..icons import icon_list_mode_items, icon_list_mode_list
from ..literals import MESSAGE_SQLITE_WARNING
from ..utils import check_for_sqlite, return_attrib

logger = logging.getLogger(__name__)
register = Library()


@register.simple_tag(takes_context=True)
def common_calculate_title(context):
    if context.get('title'):
        title_full = context.get('title')
        title = truncatechars(
            title_full, arg=setting_max_title_length.value
        )
    else:
        if context.get('delete_view'):
            title = _('Confirm delete')
            title_full = title
        else:
            if context.get('form'):
                if context.get('object'):
                    title = _('Edit %s') % context.get('object')
                    title_full = title
                else:
                    title = _('Confirm')
                    title_full = title
            else:
                if context.get('read_only'):
                    title = _('Details for: %s') % context.get('object')
                    title_full = title
                else:
                    if context.get('object'):
                        title = _('Edit: %s') % context.get('object')
                        title_full = title
                    else:
                        title = _('Create')
                        title_full = title

    return {'title': title, 'title_full': title_full}


@register.simple_tag
def common_check_sqlite():
    if check_for_sqlite():
        return MESSAGE_SQLITE_WARNING


@register.simple_tag(takes_context=True)
def common_get_list_mode_icon(context):
    if context.get('list_as_items', False):
        return icon_list_mode_list
    else:
        return icon_list_mode_items


@register.simple_tag(takes_context=True)
def common_get_list_mode_querystring(context):
    try:
        request = context.request
    except AttributeError:
        # Simple request extraction failed. Might not be a view context.
        # Try alternate method.
        try:
            request = Variable('request').resolve(context)
        except VariableDoesNotExist:
            # There is no request variable, most probable a 500 in a test
            # view. Don't return any resolved request.
            logger.warning('No request variable, aborting request resolution')
            return ''

    # We do this to get an mutable copy we can modify
    querystring = request.GET.copy()

    list_as_items = context.get('list_as_items', False)

    if list_as_items:
        querystring['_list_mode'] = 'list'
    else:
        querystring['_list_mode'] = 'items'

    return '?{}'.format(querystring.urlencode())


@register.simple_tag
def common_get_object_verbose_name(obj):
    try:
        return obj._meta.verbose_name
    except AttributeError:
        if isinstance(obj, string_types):
            return ''
        else:
            return type(obj)


@register.simple_tag
def common_get_missing_items():
    return MissingItem.get_missing()


@register.filter
def common_get_type(value):
    return force_text(type(value))


@register.filter
def common_object_property(value, arg):
    return return_attrib(value, arg)


@register.simple_tag
def common_project_information(attribute_name):
    return getattr(mayan, attribute_name)


@register.simple_tag(takes_context=True)
def common_render_subtemplate(context, template_name, template_context):
    """
    Renders the specified template with the mixed parent and
    subtemplate contexts
    """
    new_context = Context(context.flatten())
    new_context.update(Context(template_context))
    return get_template(template_name).render(new_context.flatten())
