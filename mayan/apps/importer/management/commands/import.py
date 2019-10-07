from __future__ import unicode_literals

import csv
import time

from django.apps import apps
from django.core import management
from django.core.files import File

from ...tasks import task_upload_new_document


class Command(management.BaseCommand):
    help = 'Import documents from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--document_type_column',
            action='store', dest='document_type_column', default=0,
            help='Column that contains the document type labels. Column '
            'numbers start at 0.',
            type=int
        )
        parser.add_argument(
            '--document_path_column',
            action='store', dest='document_path_column', default=1,
            help='Column that contains the path to the document files. Column '
            'numbers start at 0.',
            type=int
        )
        parser.add_argument(
            '--ignore_errors',
            action='store_true', dest='ignore_errors', default=False,
            help='Don\'t stop the import process on common errors like '
            'incorrect file paths.',
        )
        parser.add_argument(
            '--ignore_rows',
            action='store', dest='ignore_rows', default='',
            help='Ignore a set of rows. Row numbers must be separated by commas.'
        )
        parser.add_argument(
            '--metadata_pairs_column',
            action='store', dest='metadata_pairs_column',
            help='Column that contains metadata name and values for the '
            'documents. Use the form: <label column>:<value column>. Example: '
            '2:5. Separate multiple pairs with commas. Example: 2:5,7:10',
        )
        parser.add_argument('filelist', nargs='?', help='File list')

    def handle(self, *args, **options):
        time_start = time.time()
        time_last_display = time_start
        document_types = {}
        uploaded_count = 0
        row_count = 0
        rows_to_ignore = []
        for entry in options['ignore_rows'].split(','):
            if entry:
                rows_to_ignore.append(int(entry))

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
            with open(options['filelist'], mode='r') as csv_datafile:
                csv_reader = csv.reader(
                    csv_datafile, delimiter=',', quotechar='"'
                )
                for row in csv_reader:
                    # Increase row count here even though start index is 0
                    # purpose is to avoid losing row number increments on
                    # exceptions
                    row_count = row_count + 1
                    if row_count - 1 not in rows_to_ignore:
                        try:
                            with open(row[options['document_path_column']], mode='rb') as file_object:
                                document_type_label = row[options['document_type_column']]

                                if document_type_label not in document_types:
                                    self.stdout.write(
                                        'New document type: {}. Creating and caching.'.format(
                                            document_type_label
                                        )
                                    )
                                    document_type, created = DocumentType.objects.get_or_create(
                                        label=document_type_label
                                    )
                                    document_types[document_type_label] = document_type
                                else:
                                    document_type = document_types[document_type_label]

                                shared_uploaded_file = SharedUploadedFile.objects.create(
                                    file=File(file_object)
                                )

                                extra_data = {}
                                if options['metadata_pairs_column']:
                                    extra_data['metadata_pairs'] = []

                                    for pair in options['metadata_pairs_column'].split(','):
                                        name, value = pair.split(':')
                                        extra_data['metadata_pairs'].append(
                                            {
                                                'name': row[int(name)],
                                                'value': row[int(value)]
                                            }
                                        )

                                task_upload_new_document.apply_async(
                                    kwargs=dict(
                                        document_type_id=document_type.pk,
                                        shared_uploaded_file_id=shared_uploaded_file.pk,
                                        extra_data=extra_data
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

                        except (IOError, OSError) as exception:
                            if not options['ignore_errors']:
                                raise
                            else:
                                self.stderr.write(
                                    'Error processing row: {}; {}.'.format(
                                        row_count - 1, exception
                                    )
                                )

            self.stdout.write(
                'Total files copied and queues: {}'.format(uploaded_count)
            )
            self.stdout.write(
                'Total time: {}'.format(time.time() - time_start)
            )
