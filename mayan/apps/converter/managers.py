from __future__ import unicode_literals

from ast import literal_eval
import logging

from django.contrib.contenttypes.models import ContentType
from django.db import models

from .classes import BaseTransformation

logger = logging.getLogger(__name__)


class TransformationManager(models.Manager):
    def get_for_model(self, obj, as_classes=False):
        """
        as_classes == True returns the transformation classes from .classes
        ready to be feed to the converter class
        """

        content_type = ContentType.objects.get_for_model(obj)

        transformations = self.filter(content_type=content_type, object_id=obj.pk)

        if as_classes:
            result = []
            for transformation in transformations:
                try:
                    transformation_class = BaseTransformation.get(transformation.name)
                except KeyError:
                    # Non existant transformation, but we don't raise an error
                    logger.error('Non existant transformation: %s for %s', transformation.name, obj)
                else:
                    # TODO: what to do if literal_eval fails?
                    result.append(transformation_class(**literal_eval(transformation.arguments)))

            return result
        else:
            return transformations



