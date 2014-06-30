object_navigation = {}
multi_object_navigation = {}
model_list_columns = {}
sidebar_templates = {}
top_menu_entries = []


def register_multi_item_links(src, links, menu_name=None):
    """
    Register a multiple item action action to be displayed in the
    generic list template
    """

    multi_object_navigation.setdefault(menu_name, {})
    if hasattr(src, '__iter__'):
        for one_src in src:
            multi_object_navigation[menu_name].setdefault(one_src, {'links': []})
            multi_object_navigation[menu_name][one_src]['links'].extend(links)
    else:
        multi_object_navigation[menu_name].setdefault(src, {'links': []})
        multi_object_navigation[menu_name][src]['links'].extend(links)


def register_links(src, links, menu_name=None, position=None):
    """
    Associate a link to a model a view, or an url
    """

    object_navigation.setdefault(menu_name, {})
    if hasattr(src, '__iter__'):
        for one_src in src:
            object_navigation[menu_name].setdefault(one_src, {'links': []})
            if position is not None:
                for link in reversed(links):
                    object_navigation[menu_name][one_src]['links'].insert(position, link)
            else:
                object_navigation[menu_name][one_src]['links'].extend(links)
    else:
        object_navigation[menu_name].setdefault(src, {'links': []})
        if position is not None:
            for link in reversed(links):
                object_navigation[menu_name][src]['links'].insert(position, link)
        else:
            object_navigation[menu_name][src]['links'].extend(links)


def register_top_menu(name, link, children_views=None,
                      children_path_regex=None, children_view_regex=None,
                      position=None):
    """
    Register a new menu entry for the main menu displayed at the top
    of the page
    """

    entry = {'link': link, 'name': name}
    if children_views:
        entry['children_views'] = children_views
    if children_path_regex:
        entry['children_path_regex'] = children_path_regex
    if children_view_regex:
        entry['children_view_regex'] = children_view_regex
    if position is not None:
        entry['position'] = position
        top_menu_entries.insert(position, entry)
    else:
        length = len(top_menu_entries)
        entry['position'] = length
        top_menu_entries.append(entry)

    sort_menu_entries()

    return entry


def sort_menu_entries():
    global top_menu_entries
    top_menu_entries = sorted(top_menu_entries, key=lambda k: (k['position'] < 0, k['position']))


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
