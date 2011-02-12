import copy

from django.db.utils import DatabaseError

from permissions.utils import has_permission
from permissions.models import Permission


object_navigation = {}
menu_links = []
model_list_columns = {}

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


def register_model_list_columns(model, columns):
    if model in model_list_columns:
        model_list_columns[model].extend(columns)
    else:
        model_list_columns[model] = copy.copy(columns)


def register_permissions(app, permissions):
    if permissions:
        for permission in permissions:
            full_permission_name =  "%s_%s" % (app, permission['name'])
            try:
                #if not Permission.objects.filter(codename=full_permission_name):
                #    Permission(name=unicode(permission['label']), codename=full_permission_name).save()
                permission_obj, created = Permission.objects.get_or_create(codename=full_permission_name)
                permission_obj.name=unicode(permission['label'])
                permission_obj.save()
            except DatabaseError:
                #Special case for ./manage.py syncdb
                pass


def check_permissions(object, user, permission_list):
    temp_role = []
    for permission in permission_list:
        if has_permission(object, user, permission):
            return True
