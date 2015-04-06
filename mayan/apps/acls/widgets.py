from __future__ import unicode_literals

from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase


def object_indentifier(obj):
    content_type = ContentType.objects.get_for_model(obj)

    ct_fullname = '%s.%s' % (content_type.app_label, content_type.name)
    if isinstance(obj, ModelBase):
        label = getattr(obj._meta, 'verbose_name_plural', unicode(content_type))
    else:
        if ct_fullname == 'auth.user':
            label = obj.get_full_name()
        else:
            label = unicode(obj)

    return mark_safe('<span>{}</span>'.format(label))
