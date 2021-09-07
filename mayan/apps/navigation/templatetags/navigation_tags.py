from django.template import Library

from ..classes import Menu, SourceColumn

register = Library()


def _navigation_resolve_menu(context, name, source=None, sort_results=None):
    result = []

    menu = Menu.get(name)
    link_groups = menu.resolve(
        context=context, source=source, sort_results=sort_results
    )

    if link_groups:
        result.append(
            {
                'link_groups': link_groups, 'menu': menu
            }
        )

    return result


@register.simple_tag(takes_context=True)
def navigation_get_sort_field_querystring(context, column):
    return column.get_sort_field_querystring(context=context)


@register.simple_tag
def navigation_get_source_columns(
    source, exclude_identifier=False, names=None, only_identifier=False
):
    return SourceColumn.get_for_source(
        source=source, exclude_identifier=exclude_identifier,
        names=names, only_identifier=only_identifier
    )


@register.simple_tag(takes_context=True)
def navigation_resolve_menu(context, name, source=None, sort_results=None):
    return _navigation_resolve_menu(
        context=context, name=name, source=source, sort_results=sort_results
    )


@register.simple_tag(takes_context=True)
def navigation_resolve_menus(context, names, source=None, sort_results=None):
    result = []

    for name in names.split(','):
        result.extend(
            _navigation_resolve_menu(
                context=context, name=name, source=source, sort_results=sort_results
            )
        )

    return result


@register.simple_tag(takes_context=True)
def navigation_source_column_get_sort_icon(context, column):
    if column:
        result = column.get_sort_icon(context=context)
        return result
    else:
        return ''


@register.simple_tag(takes_context=True)
def navigation_source_column_resolve(context, column):
    if column:
        result = column.resolve(context=context)
        return result
    else:
        return ''
