from __future__ import absolute_import

import os
import sys
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError, LabelCommand
from django.utils.simplejson import loads

from metadata.api import convert_dict_to_dict_list
from documents.models import DocumentType

from ...models import OutOfProcess
from ...compressed_file import CompressedFile, NotACompressedFile


class Command(LabelCommand):
    args = '<filename>'
    help = 'Upload documents from a compressed file in to the database.'
    option_list = LabelCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive',
            default=True, help='Do not ask the user for confirmation before '
                'starting.'),
        make_option('--metadata', action='store', dest='metadata',
            help='A metadata dictionary list to apply to the documents.'),
        make_option('--document_type', action='store', dest='document_type_name',
            help='The document type to apply to the uploaded documents.'),
    )

    def handle_label(self, label, **options):
        if not os.access(label, os.R_OK):
            raise CommandError("File '%s' is not readable." % label)

        if options['metadata']:
            try:
                metadata_dict = loads(options['metadata'])
                metadata_dict_list = convert_dict_to_dict_list(metadata_dict)
            except Exception, e:
                sys.exit('Metadata error: %s' % e)
        else:
            metadata_dict_list = None

        if options['document_type_name']:
            try:
                document_type = DocumentType.objects.get(name=options['document_type_name'])
            except DocumentType.DoesNotExist:
                sys.exit('Unknown document type')
        else:
            document_type = None

        if _confirm(options['interactive']) == 'yes':
            print 'Beginning upload...'
            if metadata_dict_list:
                print 'Using the metadata values:'
                for key, value in metadata_dict.items():
                    print '%s: %s' % (key, value)

            if document_type:
                print 'Uploaded document will be of type: %s' % options['document_type_name']

            source = OutOfProcess()
            fd = open(label)
            try:
                result = source.upload_file(fd, filename=None, use_file_name=False, document_type=document_type, expand=True, metadata_dict_list=metadata_dict_list, user=None, document=None, new_version_data=None, command_line=True)
                pass
            except NotACompressedFile:
                print '%s is not a compressed file.' % label
            else:
                print 'Finished.'

            fd.close()
        else:
            print 'Cancelled.'


def _confirm(interactive):
    if not interactive:
        return 'yes'
    return raw_input('You have requested to bulk upload a number of documents from a compressed file.\n' 
            'Are you sure you want to do this?\n'
            'Type \'yes\' to continue, or any other value to cancel: ')
