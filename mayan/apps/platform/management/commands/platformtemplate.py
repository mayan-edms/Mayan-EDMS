from __future__ import unicode_literals

from django.core import management

from ...classes import PlatformTemplate


class Command(management.BaseCommand):
    help = 'Render a platform configuration template.'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='?', help='Template name')
        parser.add_argument(
            '--list', action='store_true', dest='list',
            help='Show a list of available templates.',
        )
        parser.add_argument(
            '--context', action='store', default='', dest='context',
            help='Pass a context to the template in the form of a JSON encoded '
            'dictionary.',
        )

    def handle(self, *args, **options):
        if options.get('list'):
            self.stdout.write('\nAvailable platform templates.')
            self.stdout.write('----')
            for template_class in PlatformTemplate.all():
                template = template_class()
                self.stdout.write(
                    '* {}\t{}'.format(template.name, template.get_label())
                )

            self.stdout.write('\n')
        else:
            try:
                template = PlatformTemplate.get(name=options['name'])
            except KeyError:
                self.stderr.write(
                    'Unknown template "{}".'.format(options['name'])
                )
                exit(1)
            else:
                self.stdout.write(template().render(
                    context_string=options.get('context'))
                )
