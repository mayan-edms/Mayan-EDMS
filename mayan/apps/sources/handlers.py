from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from converter.models import Transformation

from .literals import SOURCE_UNCOMPRESS_CHOICE_ASK


def create_default_document_source(sender, **kwargs):
    WebFormSource = sender.get_model('WebFormSource')

    if not WebFormSource.objects.count():
        WebFormSource.objects.create(
            label=_('Default'), uncompress=SOURCE_UNCOMPRESS_CHOICE_ASK
        )


def copy_transformations_to_version(sender, **kwargs):
    Transformation = sender.get_model('Transformation')

    instance = kwargs['instance']

    # TODO: Fix this, source should be previous version
    # TODO: Fix this, shouldn't this be at the documents app
    Transformation.objects.copy(
        source=instance.document, targets=instance.pages.all()
    )


def initialize_periodic_tasks(sender, **kwargs):
    POP3Email = sender.get_model('POP3Email')
    IMAPEmail = sender.get_model('IMAPEmail')
    WatchFolderSource = sender.get_model('WatchFolderSource')

    for source in POP3Email.objects.filter(enabled=True):
        source.save()

    for source in IMAPEmail.objects.filter(enabled=True):
        source.save()

    for source in WatchFolderSource.objects.filter(enabled=True):
        source.save()
