from django.apps import apps
from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as DjangoCommand
)


class Command(DjangoCommand):
    help = 'Call the collectstatic command with some specific defaults.'

    def handle(self, **options):
        """
        Collect static_media_ignore_patterns from all apps. The pattern
        matches anything after "/<app name>/static/"
        """
        self.verbosity = options['verbosity']

        for key, data in apps.app_configs.items():
            options['ignore_patterns'].extend(getattr(data, 'static_media_ignore_patterns', ()))

        if options['verbosity'] >= 1:
            self.log('Ignore patterns: {}'.format(options['ignore_patterns']), level=1)

        return super().handle(**options)
