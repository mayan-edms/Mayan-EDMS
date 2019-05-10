from __future__ import unicode_literals

import logging

import yaml

try:
    from yaml import CSafeLoader as SafeLoader, CDumper as Dumper
except ImportError:
    from yaml import SafeLoader, Dumper

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction

from .transformations import BaseTransformation

logger = logging.getLogger(__name__)


class TransformationManager(models.Manager):
    def add_to_object(self, obj, transformation, arguments=None):
        content_type = ContentType.objects.get_for_model(model=obj)

        self.create(
            content_type=content_type, object_id=obj.pk,
            name=transformation.name, arguments=yaml.dump(
                data=arguments, Dumper=Dumper
            )
        )

    def copy(self, source, targets):
        """
        Copy transformation from source to all targets
        """
        content_type = ContentType.objects.get_for_model(model=source)

        # Get transformations
        transformations = self.filter(
            content_type=content_type, object_id=source.pk
        ).values('name', 'arguments', 'order')
        logger.debug('source transformations: %s', transformations)

        # Get all targets from target QS
        targets_dict = map(
            lambda entry: {
                'content_type': entry[0], 'object_id': entry[1]
            }, zip(
                ContentType.objects.get_for_models(models=targets).values(),
                targets.values_list('pk', flat=True)
            )
        )
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
        with transaction.atomic():
            self.bulk_create(
                map(lambda entry: self.model(**entry), results),
            )

    def get_for_object(self, obj, as_classes=False):
        """
        as_classes == True returns the transformation classes from .classes
        ready to be feed to the converter class
        """
        content_type = ContentType.objects.get_for_model(model=obj)

        transformations = self.filter(
            content_type=content_type, object_id=obj.pk
        )

        if as_classes:
            result = []
            for transformation in transformations:
                try:
                    transformation_class = BaseTransformation.get(
                        transformation.name
                    )
                except KeyError:
                    # Non existant transformation, but we don't raise an error
                    logger.error(
                        'Non existant transformation: %s for %s',
                        transformation.name, obj
                    )
                else:
                    try:
                        # Some transformations don't require arguments
                        # return an empty dictionary as ** doesn't allow None
                        if transformation.arguments:
                            kwargs = yaml.load(
                                stream=transformation.arguments,
                                Loader=SafeLoader
                            )
                        else:
                            kwargs = {}

                        result.append(
                            transformation_class(
                                **kwargs
                            )
                        )
                    except Exception as exception:
                        logger.error(
                            'Error while parsing transformation "%s", '
                            'arguments "%s", for object "%s"; %s',
                            transformation, transformation.arguments, obj,
                            exception
                        )

            return result
        else:
            return transformations
