from ast import literal_eval

from django.db import models
from django.contrib.contenttypes.models import ContentType


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
