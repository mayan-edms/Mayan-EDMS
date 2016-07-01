from __future__ import unicode_literals

from django.apps import apps
from django.core.management.color import no_style
from django.db import DEFAULT_DB_ALIAS, connections, router

from .literals import DEFAULT_ORGANIZATION_LABEL


def create_default_organization(verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, **kwargs):
    """
    Creates the default Organization object.
    """

    try:
        Organization = apps.get_model('organizations', 'Organization')
    except LookupError:
        return

    if not router.allow_migrate(using, Organization):
        return

    if not Organization.objects.using(using).exists():
        # The default settings set ORGANIZATION_ID = 1, and some tests in Django's test
        # suite rely on this value. However, if database sequences are reused
        # (e.g. in the test suite after flush/syncdb), it isn't guaranteed that
        # the next id will be 1, so we coerce it. See #15573 and #16353. This
        # can also crop up outside of tests - see #15346.
        if verbosity >= 2:
            print('Creating default Organization object')
        Organization(pk=1, label=DEFAULT_ORGANIZATION_LABEL).save(using=using)

        # We set an explicit pk instead of relying on auto-incrementation,
        # so we need to reset the database sequence. See #17415.
        sequence_sql = connections[using].ops.sequence_reset_sql(
            no_style(), [Organization]
        )
        if sequence_sql:
            if verbosity >= 2:
                print('Resetting sequence')
            with connections[using].cursor() as cursor:
                for command in sequence_sql:
                    cursor.execute(command)

        Organization.objects.clear_cache()

        return Organization.objects.get(pk=1)
