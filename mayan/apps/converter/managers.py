import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.serialization import yaml_load

from .classes import Layer
from .transformations import BaseTransformation

logger = logging.getLogger(name=__name__)


class LayerTransformationManager(models.Manager):
    def get_for_object(
        self, obj, as_classes=False, maximum_layer_order=None,
        only_stored_layer=None, user=None
    ):
        """
        as_classes == True returns the transformation classes from .classes
        ready to be feed to the converter class
        """
        Layer.update()

        StoredLayer = apps.get_model(
            app_label='converter', model_name='StoredLayer'
        )
        content_type = ContentType.objects.get_for_model(model=obj)

        transformations = self.filter(
            enabled=True, object_layer__content_type=content_type,
            object_layer__object_id=obj.pk, object_layer__enabled=True
        )

        access_layers = StoredLayer.objects.all()
        exclude_layers = StoredLayer.objects.none()

        if maximum_layer_order:
            access_layers = StoredLayer.objects.filter(
                order__lte=maximum_layer_order
            )
            exclude_layers = StoredLayer.objects.filter(
                order__gt=maximum_layer_order
            )

        for stored_layer in access_layers:
            try:
                layer_class = stored_layer.get_layer()
            except KeyError:
                """
                This was a class defined but later erased. Ignore it.
                """
            else:
                access_permission = layer_class.permissions.get(
                    'access_permission', None
                )
                if access_permission:
                    try:
                        AccessControlList.objects.check_access(
                            obj=obj, permissions=(access_permission,), user=user
                        )
                    except PermissionDenied:
                        access_layers = access_layers.exclude(pk=stored_layer.pk)

        for stored_layer in exclude_layers:
            exclude_permission = stored_layer.get_layer().permissions.get(
                'exclude_permission', None
            )
            if exclude_permission:
                try:
                    AccessControlList.objects.check_access(
                        obj=obj, permissions=(exclude_permission,), user=user
                    )
                except PermissionDenied:
                    pass
                else:
                    exclude_layers = exclude_layers.exclude(pk=stored_layer.pk)

        if only_stored_layer:
            transformations = transformations.filter(
                object_layer__stored_layer=only_stored_layer
            )

        transformations = transformations.filter(
            object_layer__stored_layer__in=access_layers
        )

        transformations = transformations.exclude(
            object_layer__stored_layer__in=exclude_layers
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
                            kwargs = yaml_load(
                                stream=transformation.arguments,
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


class ObjectLayerManager(models.Manager):
    def get_for(self, layer, obj):
        content_type = ContentType.objects.get_for_model(model=obj)

        return self.get_or_create(
            content_type=content_type, object_id=obj.pk,
            stored_layer=layer.stored_layer
        )
