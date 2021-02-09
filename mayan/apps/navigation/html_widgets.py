from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

from mayan.apps.templating.classes import Template


class SourceColumnWidget:
    template_name = None
    template_string = None

    def __init__(self, column, request):
        self.column = column
        self.request = request

    def get_extra_context(self):
        return {}

    def get_template_name(self):
        return self.template_name

    def get_template_string(self):
        return self.template_string

    def render(self, value=None):
        template_name = self.get_template_name()
        template_string = self.get_template_string()

        self.value = value
        context = {
            'column': self.column, 'value': value
        }
        context.update(self.get_extra_context())

        if template_name:
            return render_to_string(
                template_name=self.template_name, context=context
            )
        elif template_string:
            return Template(template_string=template_string).render(context=context)
        else:
            raise ImproperlyConfigured(
                'SourceColumnWidget `{}` must provide either '
                '`template_name`, `template_string`, `get_template_name()`, '
                'or `get_template_string()`.'.format(
                    self.__class__.__name__
                )
            )


class SourceColumnLinkWidget(SourceColumnWidget):
    template_name = 'navigation/source_column_link_widget.html'
