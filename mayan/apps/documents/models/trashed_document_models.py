from ..managers import TrashCanManager

from .document_models import Document

__all__ = ('DeletedDocument',)


class DeletedDocument(Document):
    objects = TrashCanManager()

    class Meta:
        proxy = True
