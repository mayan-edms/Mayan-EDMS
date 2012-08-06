from __future__ import absolute_import

from documents.models import Document

from .api import make_trashable

make_trashable(Document)
