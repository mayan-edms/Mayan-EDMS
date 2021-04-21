from django.template import Library

from ..classes import Menu, SourceColumn

register = Library()


@register.simple_tag(takes_context=True)
def navigation_get_sort_field_querystring(context, column):
    return column.get_sort_field_querystring(context=context)


@register.simple_tag
def navigation_get_source_columns(
    source, exclude_identifier=False, only_identifier=False
):
    try:
        # Is it a query set?
        source = source.model
    except AttributeError:
        # Is not a query set
        try:
            # Is iterable?
            source = source[0]
        except TypeError:
            """
            It is not an iterable.
            """
        except IndexError:
            """
            Its a list and it's empty.
            """
        except KeyError:
            """
            Its a list and it's empty.
            """

    return SourceColumn.get_for_source(
        source=source, exclude_identifier=exclude_identifier,
        only_identifier=only_identifier
    )


@register.simple_tag(takes_context=True)
def navigation_resolve_menu(context, name, source=None, sort_results=None):
    result = []

    menu = Menu.get(name)
    link_groups = menu.resolve(
        context=context, source=source, sort_results=sort_results
    )

    if link_groups:
        result.append({'link_groups': link_groups, 'menu': menu})

    return result


@register.simple_tag(takes_context=True)
def navigation_resolve_menus(context, names, source=None, sort_results=None):
    result = []

    for name in names.split(','):
        menu = Menu.get(name=name)
        link_groups = menu.resolve(context=context, sort_results=sort_results)

        if link_groups:
            result.append({'link_groups': link_groups, 'menu': menu})

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
