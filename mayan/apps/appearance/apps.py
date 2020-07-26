from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class AppearanceApp(MayanAppConfig):
    app_url = 'appearance'
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.appearance'
    static_media_ignore_patterns = (
        'AUTHORS*', 'CHANGE*', 'CONTRIBUT*', 'CODE_OF_CONDUCT*', 'Grunt*',
        'LICENSE*', 'MAINTAIN*', 'README*', '*.less', '*.md', '*.nupkg',
        '*.nuspec', '*.scss*', '*.sh', '*tests*', 'bower*', 'composer.json*',
        'demo*', 'grunt*', 'gulp*', 'install', 'less', 'package.json*',
        'package-lock*', 'test', 'tests', 'variable*',
        'appearance/node_modules/@fancyapps/fancybox/docs/*',
        'appearance/node_modules/@fancyapps/fancybox/src/*',
        'appearance/node_modules/@fortawesome/fontawesome-free/svgs/*',
        'appearance/node_modules/bootswatch/docs/*',
        'appearance/node_modules/jquery/src/*',
        'appearance/node_modules/jquery-form/_config.yml',
        'appearance/node_modules/jquery-form/form.jquery.json',
        'appearance/node_modules/jquery-form/docs/*',
        'appearance/node_modules/jquery-form/src/*',
        'appearance/node_modules/select2/src/*',
        'appearance/node_modules/toastr/karma.conf.js',
        'appearance/node_modules/toastr/toastr.js',
        'appearance/node_modules/toastr/toastr-icon.png',
        'appearance/node_modules/toastr/nuget/*',
    )
    verbose_name = _('Appearance')

    def ready(self):
        super(AppearanceApp, self).ready()
