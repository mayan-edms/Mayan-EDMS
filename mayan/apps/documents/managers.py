from __future__ import unicode_literals

from ast import literal_eval
import logging

from django.db import models, transaction

from common.compressed_files import CompressedFile, NotACompressedFile

from .settings import RECENT_COUNT, LANGUAGE

logger = logging.getLogger(__name__)


class DocumentPageTransformationManager(models.Manager):
    def get_for_document_page(self, document_page):
        return self.model.objects.filter(document_page=document_page)

    def get_for_document_page_as_list(self, document_page):
        warnings = []
        transformations = []
        for transformation in self.get_for_document_page(document_page).values('transformation', 'arguments'):
            try:
                transformations.append(
                    {
                        'transformation': transformation['transformation'],
                        'arguments': literal_eval(transformation['arguments'].strip())
                    }
                )
            except (ValueError, SyntaxError) as exception:
                warnings.append(exception)

        return transformations, warnings


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        if user.is_authenticated():
            new_recent, created = self.model.objects.get_or_create(user=user, document=document)
            if not created:
                # document already in the recent list, just save to force
                # accessed date and time update
                new_recent.save()
            for recent_to_delete in self.model.objects.filter(user=user)[RECENT_COUNT:]:
                recent_to_delete.delete()

    def get_for_user(self, user):
        document_model = models.get_model('documents', 'document')

        if user.is_authenticated():
            return document_model.objects.filter(recentdocument__user=user).order_by('-recentdocument__datetime_accessed')
        else:
            return document_model.objects.none()


class DocumentTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class DocumentManager(models.Manager):
    @transaction.atomic
    def new_document(self, document_type, file_object, label=None, command_line=False, description=None, expand=False, language=None, user=None):
        versions_created = []

        if expand:
            try:
                compressed_file = CompressedFile(file_object)
                count = 1
                for compressed_file_child in compressed_file.children():
                    if command_line:
                        print 'Uploading file #%d: %s' % (count, compressed_file_child)
                    versions_created.append(self.upload_single_document(document_type=document_type, file_object=compressed_file_child, description=description, label=unicode(compressed_file_child), language=language or LANGUAGE, user=user))
                    compressed_file_child.close()
                    count += 1

            except NotACompressedFile:
                logging.debug('Exception: NotACompressedFile')
                if command_line:
                    raise
                versions_created.append(self.upload_single_document(document_type=document_type, file_object=file_object, description=description, label=label, language=language or LANGUAGE, user=user))
        else:
            versions_created.append(self.upload_single_document(document_type=document_type, file_object=file_object, description=description, label=label, language=language or LANGUAGE, user=user))

        return versions_created

    @transaction.atomic
    def upload_single_document(self, document_type, file_object, label=None, description=None, language=None, user=None):
        document = self.model(description=description, document_type=document_type, language=language, label=label or unicode(file_object))
        document.save(user=user)
        version = document.new_version(file_object=file_object, user=user)
        document.set_document_type(document_type, force=True)
        return version
