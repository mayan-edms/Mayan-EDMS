from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .literals import SOURCE_UNCOMPRESS_CHOICE_ASK
from .models import WebFormSource


def create_default_document_source(sender, **kwargs):
    WebFormSource.objects.create(title=_('Default'), uncompress=SOURCE_UNCOMPRESS_CHOICE_ASK)
