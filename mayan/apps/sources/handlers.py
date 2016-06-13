from __future__ import unicode_literals

from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from .literals import SOURCE_UNCOMPRESS_CHOICE_ASK


def create_default_document_source(sender, **kwargs):
    WebFormSource = get_model('sources', 'WebFormSource')

    if not WebFormSource.on_organization.count():
        WebFormSource.on_organization.create(
            label=_('Default'), uncompress=SOURCE_UNCOMPRESS_CHOICE_ASK
        )


def copy_transformations_to_version(sender, **kwargs):
    Transformation = get_model('converter', 'Transformation')

    instance = kwargs['instance']

    # TODO: Fix this, source should be previous version
    # TODO: Fix this, shouldn't this be at the documents app
    Transformation.objects.copy(
        source=instance.document, targets=instance.pages.all()
    )


def initialize_periodic_tasks(sender, **kwargs):
    POP3Email = get_model('sources', 'POP3Email')
    IMAPEmail = get_model('sources', 'IMAPEmail')
    WatchFolderSource = get_model('sources', 'WatchFolderSource')

    for source in POP3Email.on_organization.filter(enabled=True):
        source.save()

    for source in IMAPEmail.on_organization.filter(enabled=True):
        source.save()

    for source in WatchFolderSource.on_organization.filter(enabled=True):
        source.save()
