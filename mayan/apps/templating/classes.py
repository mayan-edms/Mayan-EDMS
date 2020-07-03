from django.template import Context, Engine, Template as DjangoTemplate


class Template:
    def __init__(self, template_name=None, template_string=None):
        self.template_name = template_name
        self.template_string = template_string

        if not template_name and not template_string:
            raise ImproperlyConfigured(
                'Must specify a template_name or a template_string.'
            )

        self._template = None

    def initialize(self):
        self.engine = Engine(
            builtins=[
                'mathfilters.templatetags.mathfilters',
                'mayan.apps.templating.templatetags.templating_tags',
            ],
            loaders = [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        )

        if self.template_name:
            self._template = self.engine.get_template(
                template_name=self.template_name
            )
        else:
            self._template = DjangoTemplate(
                engine=self.engine, template_string=self.template_string
            )

    def render(self, context=None):
        if not self._template:
            self.initialize()

        context_object = Context(dict_=context or {})

        return self._template.render(context=context_object)
