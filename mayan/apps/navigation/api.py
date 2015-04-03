from __future__ import unicode_literals

object_navigation = {}
model_list_columns = {}


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


def register_model_list_columns(model, columns):
    """
    Define which columns will be displayed in the generic list template
    for a given model
    """

    model_list_columns.setdefault(model, [])
    model_list_columns[model].extend(columns)
