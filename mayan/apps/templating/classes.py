from django.template import Context, Template as DjangoTemplate


class Template(object):
    def __init__(self, template_string):
        self.template = DjangoTemplate(template_string=template_string)

    def render(self, context=None):
        context_object = Context(dict_=context or {})

        return self.template.render(context=context_object)
