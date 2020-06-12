from django.template import Context, Engine, Template as DjangoTemplate


class Template:
    def __init__(self, template_string):
        engine = Engine(
            builtins=[
                'mathfilters.templatetags.mathfilters',
                'mayan.apps.templating.templatetags.templating_tags',
            ]
        )

        self._template = DjangoTemplate(
            engine=engine, template_string=template_string
        )

    def render(self, context=None):
        context_object = Context(dict_=context or {})

        return self._template.render(context=context_object)
