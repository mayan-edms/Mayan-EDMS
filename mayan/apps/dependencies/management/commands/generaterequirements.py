from __future__ import unicode_literals

from django.core import management
from django.utils.translation import ugettext_lazy as _

from ...classes import PythonDependency


class Command(management.BaseCommand):
    help = 'Generate Python requirement files.'

    def add_arguments(self, parser):
        parser.add_argument('environment', nargs='?', help='Environment name')
        parser.add_argument(
            '--exclude', action='store', dest='exclude', help=_(
                'Comma separated names of dependencies to exclude from the '
                'list generated.'
            ),
        )
        parser.add_argument(
            '--only', action='store', dest='only', help=_(
                'Comma separated names of dependencies to show in the list '
                'while excluding every other one.'
            ),
        )

    def handle(self, *args, **options):
        dependency_list = PythonDependency.get_for_attribute(
            attribute_name='environment__name',
            attribute_value=options['environment'], subclass_only=True
        )
        exclude_list = (options['exclude'] or '').split(',')
        only_list = (options['only'] or '').split(',')
        result = []

        for dependency in dependency_list:
            if only_list != ['']:
                if dependency.name in only_list:
                    result.append(dependency)
            else:
                result.append(dependency)

        for dependency in result:
            if dependency.name not in exclude_list:
                print(
                    '{}{}'.format(dependency.name, dependency.version_string)
                )
