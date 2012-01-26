from __future__ import absolute_import

import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError, LabelCommand

from ...models import OutOfProcess
from ...compressed_file import CompressedFile, NotACompressedFile


class Command(LabelCommand):
    args = '<filename>'
    help = 'Upload documents from a compressed file in to the database.'
    option_list = LabelCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive',
            default=True, help='Do not ask the user for confirmation before '
                'starting.'),
        #make_option('--metadata', action='store', dest='metadata',
        #    help='A metadata dictionary to apply to the documents.'),
    )
        
    def handle_label(self, label, **options):
        if not os.access(label, os.R_OK):
            raise CommandError("File '%s' is not readable." % label)

        if _confirm(options['interactive']) == 'yes':
            print 'Beginning upload...'
            fd = open(label)
            source = OutOfProcess()
            try:
                result = source.upload_file(fd, filename=None, use_file_name=False, document_type=None, expand=True, metadata_dict_list=None, user=None, document=None, new_version_data=None, verbose=True)
            except NotACompressedFile:
                print '%s is not a compressed file.'
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
