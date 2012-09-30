from __future__ import absolute_import

from ast import literal_eval

from django.db import models
from django.contrib.contenttypes.models import ContentType

#from .settings import LOG_SIZE


class SourceTransformationManager(models.Manager):
    def get_for_object(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        return self.model.objects.filter(content_type=ct).filter(object_id=obj.pk)

    def get_for_object_as_list(self, obj):
        warnings = []
        transformations = []
        for transformation in self.get_for_object(obj).values('transformation', 'arguments'):
            try:
                transformations.append(
                    {
                        'transformation': transformation['transformation'],
                        'arguments': literal_eval(transformation['arguments'].strip())
                    }
                )
            except (ValueError, SyntaxError), e:
                warnings.append(e)

        return transformations, warnings


class SourceLogManager(models.Manager):
    def save_status(self, source, status):
        new_recent = self.model(source=source, status=status)
        new_recent.save()
        content_type = ContentType.objects.get_for_model(source)
        to_delete = self.model.objects.filter(content_type=content_type, object_id=source.pk).order_by('-creation_datetime')[LOG_SIZE:]
        for recent_to_delete in to_delete:
            recent_to_delete.delete()

    def get_for_source(self, source):
        content_type = ContentType.objects.get_for_model(source)
        return self.model.objects.filter(content_type=content_type, object_id=source.pk).order_by('-creation_datetime')

    def get_latest_for(self, source):
        content_type = ContentType.objects.get_for_model(source)
        return self.model.objects.filter(content_type=content_type, object_id=source.pk).latest().creation_datetime
