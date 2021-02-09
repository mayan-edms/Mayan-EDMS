from django import apps
from django.conf import settings
from django.test.runner import DiscoverRunner

from .literals import EXCLUDE_TEST_TAG


class NullMigrationsClass():
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


class MayanTestRunner(DiscoverRunner):
    @classmethod
    def add_arguments(cls, parser):
        DiscoverRunner.add_arguments(parser)
        parser.add_argument(
            '--mayan-apps', action='store_true', default=False,
            dest='mayan_apps',
            help='Test all Mayan apps that report to have tests.'
        )
        parser.add_argument(
            '--no-exclude', action='store_true', default=False,
            dest='no_exclude',
            help='Include excluded tests.'
        )
        parser.add_argument(
            '--skip-migrations', action='store_true', default=False,
            dest='skip_migrations', help='Skip execution of '
            'migrations after creating the database.'
        )

    def __init__(self, *args, **kwargs):
        self.mayan_apps = kwargs.pop('mayan_apps')
        self.no_exclude = kwargs.pop('no_exclude')
        if kwargs.pop('skip_migrations'):
            settings.MIGRATION_MODULES = NullMigrationsClass()

        super().__init__(*args, **kwargs)

        # Test that should be excluded by default
        # To include then pass --tag=exclude to the test runner invocation
        if not self.no_exclude:
            if EXCLUDE_TEST_TAG not in self.tags:
                self.exclude_tags |= set((EXCLUDE_TEST_TAG,))

    def build_suite(self, *args, **kwargs):
        # Apps that report they have tests
        if self.mayan_apps:
            args = list(args)
            args[0] = [
                app.name for app in apps.apps.get_app_configs() if getattr(
                    app, 'has_tests', False
                )
            ]

        return super().build_suite(*args, **kwargs)
