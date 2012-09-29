from __future__ import absolute_import

import logging

from elementtree.ElementTree import Element, SubElement

from django.template import (VariableDoesNotExist, Variable)

from .utils import resolve_to_name, get_navigation_objects

multi_object_navigation = {}
model_list_columns = {}
sidebar_templates = {}
bound_links = {}
logger = logging.getLogger(__name__)
main_menu = Element('root')


def bind_links(sources, links, menu_name=None, position=0):
    """
    Associate a link to a model, a view, or an url
    """
    bound_links.setdefault(menu_name, {})
    for source in sources:
        bound_links[menu_name].setdefault(source, {'links': []})
        try:
            bound_links[menu_name][source]['links'].extend(links)
        except TypeError:
            # Try to see if links is a single link
            bound_links[menu_name][source]['links'].append(links)


def register_top_menu(name, link, position=None):
    """
    Register a new menu entry for the main menu displayed at the top
    of the page
    """
    new_menu = SubElement(main_menu, name, link=link, position=position)

    sorted_menus = sorted(main_menu.getchildren(), key=lambda k: (k.get('position') < 0, k.get('position')))
    main_menu.clear()

    for menu in sorted_menus:
        main_menu.append(menu)

    return new_menu


def register_model_list_columns(model, columns):
    """
    Define which columns will be displayed in the generic list template
    for a given model
    """

    model_list_columns.setdefault(model, [])
    model_list_columns[model].extend(columns)


def register_sidebar_template(source_list, template_name):
    for source in source_list:
        sidebar_templates.setdefault(source, [])
        sidebar_templates[source].append(template_name)


def register_multi_item_links(sources, links, menu_name=None):
    """
    Register a multiple item action action to be displayed in the
    generic list template
    """
    multi_object_navigation.setdefault(menu_name, {})
    for source in sources:
        multi_object_navigation[menu_name].setdefault(source, {'links': []})
        multi_object_navigation[menu_name][source]['links'].extend(links)


def get_context_navigation_links(context, menu_name=None, links_dict=bound_links):
    request = Variable('request').resolve(context)
    current_path = request.META['PATH_INFO']
    current_view = resolve_to_name(current_path)
    context_links = {}

    # Don't fudge with the original global dictionary
    # TODO: fix this
    links_dict = links_dict.copy()

    # Dynamic sources
    # TODO: improve name to 'injected...'
    try:
        """
        Check for and inject a temporary navigation dictionary
        """
        temp_navigation_links = Variable('temporary_navigation_links').resolve(context)
        if temp_navigation_links:
            links_dict.update(temp_navigation_links)
    except VariableDoesNotExist:
        pass

    try:
        view_links = links_dict[menu_name][current_view]['links']
        if view_links:
            context_links.setdefault(None, [])

        for link in view_links:
            context_links[None].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view))
    except KeyError:
        pass

    for resolved_object, object_properties in get_navigation_objects(context).items():
        try:
            resolved_object_reference = resolved_object
            object_links = links_dict[menu_name][type(resolved_object_reference)]['links']
            if object_links:
                context_links.setdefault(resolved_object_reference, [])

            for link in object_links:
                context_links[resolved_object_reference].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view))
        except KeyError:
            pass

    return context_links
