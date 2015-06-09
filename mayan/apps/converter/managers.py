from __future__ import unicode_literals

from ast import literal_eval
import logging

from django.contrib.contenttypes.models import ContentType
from django.db import models

from .classes import BaseTransformation

logger = logging.getLogger(__name__)


class TransformationManager(models.Manager):
    def copy(self, source, targets):
        """
        Copy transformation from source to all targets
        """
        content_type = ContentType.objects.get_for_model(source)

        # Get transformations
        transformations = self.filter(content_type=content_type, object_id=source.pk).values('name', 'arguments', 'order')
        logger.debug('source transformations: %s', transformations)

        # Get all targets from target QS
        targets_dict = map(lambda entry:{'content_type': entry[0], 'object_id': entry[1]}, zip(ContentType.objects.get_for_models(*targets).values(), targets.values_list('pk', flat=True)))
        logger.debug('targets: %s', targets_dict)

        # Combine the two
        results = []
        for instance in targets_dict:
            for transformation in transformations:
                result = instance.copy()
                result.update(transformation)
                results.append(dict(result))

        logger.debug('results: %s', results)

        # Bulk create for a single DB query
        self.bulk_create(
            map(lambda entry: self.model(**entry), results),
        )

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



