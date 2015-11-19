from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from converter.models import Transformation

from .literals import SOURCE_UNCOMPRESS_CHOICE_ASK
from .models import POP3Email, IMAPEmail, WatchFolderSource, WebFormSource


def create_default_document_source(sender, **kwargs):
    if not WebFormSource.objects.count():
        WebFormSource.objects.create(
            label=_('Default'), uncompress=SOURCE_UNCOMPRESS_CHOICE_ASK
        )


def copy_transformations_to_version(sender, **kwargs):
    instance = kwargs['instance']

    # TODO: Fix this, source should be previous version
    # TODO: Fix this, shouldn't this be at the documents app
    Transformation.objects.copy(
        source=instance.document, targets=instance.pages.all()
    )


def initialize_periodic_tasks(**kwargs):
    for source in POP3Email.objects.filter(enabled=True):
        source.save()

    for source in IMAPEmail.objects.filter(enabled=True):
        source.save()

    for source in WatchFolderSource.objects.filter(enabled=True):
        source.save()
