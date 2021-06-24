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
