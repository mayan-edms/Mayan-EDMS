from __future__ import absolute_import

from ast import literal_eval

from django.db import models
from django.contrib.contenttypes.models import ContentType

from .conf.settings import POP3_EMAIL_LOG_SIZE


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


class POP3EmailLogManager(models.Manager):
    def save_status(self, pop3_email, status):
        new_recent = self.model(pop3_email=pop3_email, status=status)
        new_recent.save()
        to_delete = self.model.objects.filter(pop3_email=pop3_email).order_by('-creation_datetime')[POP3_EMAIL_LOG_SIZE:]
        for recent_to_delete in to_delete:
            recent_to_delete.delete()
