from __future__ import unicode_literals

object_navigation = {}
model_list_columns = {}
top_menu_entries = []


def register_links(src, links, menu_name=None, position=None):
    """
    Associate a link to a model a view, or an url
    """

    object_navigation.setdefault(menu_name, {})
    if isinstance(src, list):
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


def register_top_menu(name, link, position=None):
    """
    Register a new menu entry for the main menu displayed at the top
    of the page
    """

    entry = {'link': link, 'name': name}
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
