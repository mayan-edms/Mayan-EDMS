from __future__ import absolute_import

import csv
import os
import sys
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError, LabelCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


class Command(LabelCommand):
    args = '<filename>'
    help = 'Import users from a CSV file with the field order: username, firstname, lastname, email.'
    option_list = LabelCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive',
            default=True, help='Do not ask the user for confirmation before '
                'starting.'),
        make_option('--password', action='store', dest='password',
            help='The default password to assign to each new user.'),
        make_option('--skip-repeated', action='store_true', dest='skip_repeated',
            default=False, help='Don\'t exit if the user already exists.'),
    )

    def handle_label(self, label, **options):
        if not os.access(label, os.R_OK):
            raise CommandError("File '%s' is not readable." % label)

        if options['password']:
            default_password = options['password']
        else:
            default_password = None

        if _confirm(options['interactive']) == 'yes':
            print 'Beginning import...'
            with open(label, 'rb') as f:
                reader = unicode_csv_reader(f)
                try:
                    for row in reader:
                        print 'Adding: %s' % ', '.join(row)
                        try:
                            user = User(
                                username=row[0],
                                first_name=row[1],
                                last_name=row[2],
                                email=row[3]
                            )
                            user.set_password(default_password)
                            user.save()
                        except IntegrityError:
                            print 'Repeated user entry: %s' % ', '.join(row)
                            if options['skip_repeated']:
                                print 'Ignoring.'
                            else:
                                sys.exit()

                except csv.Error, e:
                    sys.exit('file %s, line %d: %s' % (label, reader.line_num, e))
                else:
                    print 'Finish.'
        else:
            print 'Cancelled.'


def _confirm(interactive):
    if not interactive:
        return 'yes'
    return raw_input('You have requested to import a number of users from a CSV file.\n' 
            'Are you sure you want to do this?\n'
            'Type \'yes\' to continue, or any other value to cancel: ')
