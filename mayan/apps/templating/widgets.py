from django import forms
from django.contrib import admindocs
from django.utils.translation import gettext as _
from mayan.apps.common.classes import ModelAttribute
from mayan.apps.views.widgets import NamedMultiWidget

from .classes import Template
from .literals import EMPTY_LABEL


class TemplateWidget(NamedMultiWidget):
    builtin_excludes = {
        'tags': ('csrf_token',)
    }

    subwidgets = {
        'builtin_tags': forms.widgets.Select(
            attrs={
                'data-autocopy': 'true',
                'data-field-template': '${ $this.val() }',
            }
        ),
        'template': forms.widgets.Textarea(
            attrs={'rows': 5, 'data-template-fields': 'template'}
        )
    }

    class Media:
        js = ('templating/js/template_widget.js',)

    def get_builtin_choices(self, klass, name_template='{}'):
        result = []
        template = Template('')
        builtin_libraries = [
            ('', library) for library in template._template.engine.template_builtins
        ]
        for module_name, library in builtin_libraries:
            for name, function in getattr(library, klass).items():
                if name not in self.builtin_excludes.get(klass, ()):
                    title, body, metadata = admindocs.utils.parse_docstring(
                        function.__doc__
                    )
                    title = _(title)
                    result.append(
                        (
                            name_template.format(name), '{} - {}'.format(name, title)
                        )
                    )

        result = sorted(result, key=lambda x: x[0])

        return result

    def get_context(self, name, value, attrs):
        result = super().get_context(name=name, value=value, attrs=attrs)
        # Set builtin_tags autocopy sub widget as not required
        result['widget']['subwidgets'][0]['attrs']['required'] = False
        return result

    def decompress(self, value):
        choices_builtin = []
        choices_builtin.append(
            (
                _('Filters'), self.get_builtin_choices(
                    klass='filters', name_template='{{{{ | {} }}}}'
                )
            )
        )
        choices_builtin.append(
            (
                _('Tags'), self.get_builtin_choices(
                    klass='tags', name_template='{{% {} %}}'
                )
            )
        )
        choices_builtin.insert(
            0, ('', _('<Filters and tags>'))
        )

        self.widgets['builtin_tags'].choices = choices_builtin
        return {
            'builtin_tags': None, 'template': value
        }

    def value_from_datadict(self, querydict, files, name):
        template = querydict.get('{}_template'.format(name))

        return template


class ModelTemplateWidget(TemplateWidget):
    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs=attrs, **kwargs)
        self.widgets['model_attribute'] = forms.widgets.Select(
            attrs={
                'data-autocopy': 'true',
                'data-field-template': '{{ ${ $idTemplate.data("model-variable") }.${ $this.val() } }}'
            }
        )
        self.subwidgets_order.insert(0, 'model_attribute')

    def get_context(self, name, value, attrs):
        result = super().get_context(name=name, value=value, attrs=attrs)
        # Set model_attribute autocopy sub widget as not required
        result['widget']['subwidgets'][1]['attrs']['required'] = False
        return result

    def decompress(self, value):
        result = super().decompress(value=value)

        attribute_choices = ModelAttribute.get_all_choices_for(
            model=self.attrs['model']
        )
        attribute_choices.insert(
            0, ('', _('<Model attributes>'))
        )

        self.widgets['model_attribute'].choices = attribute_choices

        result['model_attribute'] = None

        return result
