object_navigation = {}
multi_object_navigation = {}
menu_links = []
model_list_columns = {}
sidebar_templates = {}


def register_multi_item_links(src, links, menu_name=None):
    multi_object_navigation.setdefault(menu_name, {})
    if hasattr(src, '__iter__'):
        for one_src in src:
            multi_object_navigation[menu_name].setdefault(one_src, {'links': []})
            multi_object_navigation[menu_name][one_src]['links'].extend(links)
    else:
        multi_object_navigation[menu_name].setdefault(src, {'links': []})
        multi_object_navigation[menu_name][src]['links'].extend(links)


def register_links(src, links, menu_name=None):
    object_navigation.setdefault(menu_name, {})
    if hasattr(src, '__iter__'):
        for one_src in src:
            object_navigation[menu_name].setdefault(one_src, {'links': []})
            object_navigation[menu_name][one_src]['links'].extend(links)
    else:
        object_navigation[menu_name].setdefault(src, {'links': []})
        object_navigation[menu_name][src]['links'].extend(links)


def register_menu(links):
    for link in links:
        menu_links.append(link)

    menu_links.sort(lambda x, y: 1 if x > y else -1, lambda x: x['position'] if 'position' in x else 1)


def register_model_list_columns(model, columns):
    model_list_columns.setdefault(model, [])
    model_list_columns[model].extend(columns)


def register_sidebar_template(source_list, template_name):
    for source in source_list:
        sidebar_templates.setdefault(source, [])
        sidebar_templates[source].append(template_name)
