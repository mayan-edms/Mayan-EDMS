from django.template import Library

from ..classes import Collection, Menu, SourceColumn

register = Library()


@register.simple_tag(takes_context=True)
def navigation_get_sort_field_querystring(context, column):
    return column.get_sort_field_querystring(context=context)


@register.simple_tag(takes_context=True)
def navigation_get_source_columns(context, source, exclude_identifier=False, only_identifier=False):
    try:
        # Is it a query set?
        source = source.model
    except AttributeError:
        # Is not a query set
        try:
            # Is iterable?
            source = source[0]
        except TypeError:
            # It is not an iterable
            pass
        except IndexError:
            # It a list and it's empty
            pass
        except KeyError:
            # It a list and it's empty
            pass

    return SourceColumn.get_for_source(
        context=context, source=source, exclude_identifier=exclude_identifier,
        only_identifier=only_identifier
    )


@register.simple_tag()
def navigation_link_widget_render(link):
    return link.widget(link.instance)


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
def navigation_source_column_resolve(context, column):
    if column:
        result = column.resolve(context=context)
        return result
    else:
        return ''
