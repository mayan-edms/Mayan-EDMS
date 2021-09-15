from mayan.apps.converter.exceptions import AppImageError
from mayan.apps.events.classes import EventManagerMethodAfter
from mayan.apps.events.decorators import method_event

from ..events import event_trashed_document_restored
from ..literals import IMAGE_ERROR_NO_VERSION_PAGES
from ..managers import TrashCanManager

from .document_models import Document

__all__ = ('TrashedDocument',)


class TrashedDocument(Document):
    objects = TrashCanManager()

    class Meta:
        proxy = True

    def get_api_image_url(
        self, maximum_layer_order=None, transformation_instance_list=None,
        user=None
    ):
        first_page = self.pages.first()
        if first_page:
            return first_page.get_api_image_url(
                maximum_layer_order=None, transformation_instance_list=None,
                user=user, viewname='rest_api:trasheddocument-image',
                view_kwargs={'document_id': self.pk}
            )
        else:
            raise AppImageError(error_name=IMAGE_ERROR_NO_VERSION_PAGES)

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
