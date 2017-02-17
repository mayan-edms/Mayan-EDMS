from __future__ import unicode_literals

import os

from django import apps
from django.conf import settings
from django.test.runner import DiscoverRunner


class MayanTestRunner(DiscoverRunner):
    @classmethod
    def add_arguments(cls, parser):
        DiscoverRunner.add_arguments(parser)

    def build_suite(self, *args, **kwargs):
        self.top_level = os.path.join(settings.BASE_DIR, 'apps')

        test_suit = super(MayanTestRunner, self).build_suite(*args, **kwargs)

        new_suite = self.test_suite()

        # Apps that report they have tests

        test_apps = [
            app.name for app in apps.apps.get_app_configs() if getattr(app, 'test', False)
        ]

        # Filter the test cases reported by the test runner by the apps that
        # reported tests

        for test_case in test_suit:
            app_label = repr(test_case.__class__).split("'")[1].split('.')[0]
            if app_label in test_apps:
                new_suite.addTest(test_case)

        print '-' * 10
        print 'Apps to test: {}'.format(', '.join(test_apps))
        print 'Total test cases: {}'.format(new_suite.countTestCases())
        print '-' * 10

        return new_suite
