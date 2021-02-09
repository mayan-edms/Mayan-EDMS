import hashlib

from django.template import Context, Engine, Template as DjangoTemplate
from django.template.response import TemplateResponse
from django.urls import reverse

from mayan.apps.common.settings import setting_home_view


class AJAXTemplate:
    _registry = {}

    @classmethod
    def all(cls, rendered=False, request=None):
        if not rendered:
            return cls._registry.values()
        else:
            result = []
            for template in cls._registry.values():
                result.append(template.render(request=request))
            return result

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, template_name):
        self.name = name
        self.template_name = template_name
        self.__class__._registry[name] = self

    def get_absolute_url(self):
        return reverse(
            kwargs={'name': self.name}, viewname='rest_api:template-detail'
        )

    def render(self, request):
        context = {
            'home_view': setting_home_view.value,
        }
        result = TemplateResponse(
            request=request,
            template=self.template_name,
            context=context,
        ).render()

        # Calculate the hash of the bytes version but return the unicode
        # version
        self.html = result.rendered_content.replace('\n', '')
        self.hex_hash = hashlib.sha256(result.content).hexdigest()
        return self


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
