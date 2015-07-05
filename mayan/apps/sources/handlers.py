from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from converter.models import Transformation

from .literals import SOURCE_UNCOMPRESS_CHOICE_ASK
from .models import WebFormSource


def create_default_document_source(sender, **kwargs):
    WebFormSource.objects.create(title=_('Default'), uncompress=SOURCE_UNCOMPRESS_CHOICE_ASK)


def copy_transformations_to_version(sender, **kwargs):
    instance = kwargs['instance']

    Transformation.objects.copy(source=instance.document, targets=instance.pages.all())
