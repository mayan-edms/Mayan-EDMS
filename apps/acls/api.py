from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType

_class_permissions = {}


def class_permissions(cls, permission_list):
    """
    Associate a permissions list to a class
    """
    stored_permissions = _class_permissions.setdefault(cls, [])
    stored_permissions.extend(permission_list)


def get_class_permissions_for(obj):
    """
    Return a list of permissions associated with a content type
    """
    content_type = ContentType.objects.get_for_model(obj)
    return _class_permissions.get(content_type.model_class(), [])


def get_classes():
    """
    Return a list of encapsulated classes that have been registered
    """
    return _class_permissions.keys()
