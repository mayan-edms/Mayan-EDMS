import copy

object_navigation = {}
menu_links = []

def register_links(src, links, menu_name=None):
    if menu_name in object_navigation:
        if hasattr(src, '__iter__'):
            for one_src in src:
                if one_src in object_navigation[menu_name]:
                    object_navigation[menu_name][one_src]['links'].extend(links)
                else:
                    object_navigation[menu_name][one_src]={'links':copy.copy(links)}
        else:
            if src in object_navigation[menu_name]:
                object_navigation[menu_name][src]['links'].extend(links)
            else:
                object_navigation[menu_name][src] = {'links':links}
    else:
        object_navigation[menu_name] = {}        
        if hasattr(src, '__iter__'):
            for one_src in src:
                object_navigation[menu_name][one_src] = {'links':links}
        else:
            object_navigation[menu_name] = {src:{'links':links}}
        

def register_menu(links):
    for link in links:
        menu_links.append(link)
    
    menu_links.sort(lambda x,y: 1 if x>y else -1, lambda x:x['position'] if 'position' in x else 1)
