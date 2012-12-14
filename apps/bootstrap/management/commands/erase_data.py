from __future__ import absolute_import

from optparse import make_option

from django.db import models, router, connections, DEFAULT_DB_ALIAS
from django.core.management import call_command
from django.core.management.base import NoArgsCommand, CommandError
from django.core.management.color import no_style
from django.core.management.sql import emit_post_sync_signal

from ...classes import Cleanup


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to erase. '
                'Defaults to the "default" database.'),
    )
    help = 'Erases all data in a Mayan EDMS installation.'

    def handle_noargs(self, **options):
        db = options.get('database', DEFAULT_DB_ALIAS)
        connection = connections[db]
        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive')

        self.style = no_style()

        if interactive:
            confirm = raw_input("""You have requested a erase all the data in the current Mayan EDMS installation.
This will IRREVERSIBLY ERASE all user data currently in the database,
and return each table to the state it was in after syncdb.
Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: """)
        else:
            confirm = 'yes'

        if confirm == 'yes':
            try:
                Cleanup.execute_all()
            except Exception, e:
                raise CommandError("""Unable to erase data.  Possible reasons:
  * The database isn't running or isn't configured correctly.
  * At least one of the expected database tables doesn't exist.""")
            # Emit the post sync signal. This allows individual
            # applications to respond as if the database had been
            # sync'd from scratch.
            all_models = []
            for app in models.get_apps():
                all_models.extend([
                    m for m in models.get_models(app, include_auto_created=True)
                    if router.allow_syncdb(db, m)
                ])
            emit_post_sync_signal(set(all_models), verbosity, interactive, db)

            # Reinstall the initial_data fixture.
            kwargs = options.copy()
            kwargs['database'] = db
        else:
            print 'Erase data cancelled.'
