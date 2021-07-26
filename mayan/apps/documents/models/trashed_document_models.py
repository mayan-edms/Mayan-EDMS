from furl import furl

from django.urls import reverse

from mayan.apps.converter.exceptions import AppImageError
from mayan.apps.converter.models import LayerTransformation
from mayan.apps.converter.transformations import BaseTransformation
from mayan.apps.events.classes import EventManagerMethodAfter
from mayan.apps.events.decorators import method_event

from ..events import event_trashed_document_restored

from ..managers import TrashCanManager

from .document_models import Document

__all__ = ('TrashedDocument',)


class TrashedDocument(Document):
    objects = TrashCanManager()

    class Meta:
        proxy = True

    def get_api_image_url(self, *args, **kwargs):
        version_active = self.version_active
        if version_active:
            first_page = self.pages.first()
            if first_page:
                if not first_page.content_object:
                    return '#'

                # Source object transformations first.
                transformation_list = LayerTransformation.objects.get_for_object(
                    obj=first_page.content_object, as_classes=True,
                )

                transformation_list.extend(
                    first_page.get_combined_transformation_list(*args, **kwargs)
                )
                transformations_hash = BaseTransformation.combine(
                    transformations=transformation_list
                )

                kwargs.pop('transformations', None)

                final_url = furl()
                final_url.args = kwargs
                final_url.path = reverse(
                    viewname='rest_api:trasheddocument-image', kwargs={
                        'document_id': self.pk,
                    }
                )
                final_url.args['_hash'] = transformations_hash

                return final_url.tostr()
            else:
                raise AppImageError(error_name=IMAGE_ERROR_NO_VERSION_PAGES)
        else:
            raise AppImageError(error_name=IMAGE_ERROR_NO_ACTIVE_VERSION)

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_trashed_document_restored,
        target='self',
    )
    def restore(self):
        self.in_trash = False
        # Skip the edit event at .save().
        self._event_ignore = True
        self.save(update_fields=('in_trash',))
