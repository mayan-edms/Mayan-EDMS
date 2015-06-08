from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW
)


def get_kwargs_factory(variable_name):
    def get_kwargs(context):
        content_type = ContentType.objects.get_for_model(context[variable_name])
        return {'app_label': '"{}"'.format(content_type.app_label), 'model': '"{}"'.format(content_type.model), 'object_id': '{}.pk'.format(variable_name)}

    return get_kwargs


link_transformation_create = Link(kwargs=get_kwargs_factory('content_object'), permissions=[PERMISSION_TRANSFORMATION_CREATE], text=_('Create new transformation'), view='converter:transformation_create')
link_transformation_delete = Link(args='resolved_object.pk', permissions=[PERMISSION_TRANSFORMATION_DELETE], tags='dangerous', text=_('Delete'), view='converter:transformation_delete')
link_transformation_edit = Link(args='resolved_object.pk', permissions=[PERMISSION_TRANSFORMATION_EDIT], text=_('Edit'), view='converter:transformation_edit')
link_transformation_list = Link(kwargs=get_kwargs_factory('resolved_object'), permissions=[PERMISSION_TRANSFORMATION_VIEW], text=_('Transformations'), view='converter:transformation_list')
