from __future__ import unicode_literals

import csv
import time

from django.apps import apps
from django.core import management
from django.core.files import File

from mayan.apps.documents.tasks import task_upload_new_document


class Command(management.BaseCommand):
    help = 'Import documents from a CSV file.'

    def add_arguments(self, parser):
        #parser.add_argument(
        #    '-l', '--link',
        #    action='store_true', dest='link', default=False,
        #    help='Create a symbolic link to each file instead of copying.',
        #)
        parser.add_argument('filelist', nargs='?', help='File list')

    def handle(self, *args, **options):
        time_start = time.time()
        time_last_display = time_start
        document_types = {}
        uploaded_count = 0

        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        SharedUploadedFile = apps.get_model(
            app_label='common', model_name='SharedUploadedFile'
        )

        if not options['filelist']:
            self.stderr.write('Must specify a CSV file path.')
            exit(1)
        else:
            with open(options['filelist']) as csv_datafile:
                csv_reader = csv.reader(csv_datafile)
                for row in csv_reader:
                    with open(row[1]) as file_object:
                        if row[0] not in document_types:
                            self.stdout.write('New document type: {}. Creating and caching.'.format(row[0]))
                            document_type, created = DocumentType.objects.get_or_create(
                                label=row[0]
                            )
                            document_types[row[0]] = document_type
                        else:
                            document_type = document_types[row[0]]

                        shared_uploaded_file = SharedUploadedFile.objects.create(
                            file=File(file_object)
                        )

                        task_upload_new_document.apply_async(
                            kwargs=dict(
                                document_type_id=document_type.pk,
                                shared_uploaded_file_id=shared_uploaded_file.pk,
                            )
                        )

                        uploaded_count = uploaded_count + 1

                        if (time.time() - time_last_display) > 1:
                            time_last_display = time.time()
                            self.stdout.write(
                                'Time: {}s, Files copied and queued: {}, files processed per second: {}'.format(
                                    int(time.time() - time_start),
                                    uploaded_count,
                                    uploaded_count / (time.time() - time_start)
                                )
                            )

            self.stdout.write(
                'Total files copied and queues: {}'.format(uploaded_count)
            )
            self.stdout.write(
                'Total time: {}'.format(time.time() - time_start)
            )
