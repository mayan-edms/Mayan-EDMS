from django.contrib.contenttypes.models import ContentType

_class_permissions = {}


def class_permissions(cls, permission_list):
    stored_permissions = _class_permissions.setdefault(cls, [])
    stored_permissions.extend(permission_list)


def get_class_permissions_for(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return _class_permissions.get(content_type.model_class(), [])
