from django import forms
from django.template import Library, Node, Variable

register = Library()


class StylingNode(Node):
    def __init__(self, form_name, *args, **kwargs):
        self.form_name = form_name

    def render(self, context):
        form = Variable(self.form_name).resolve(context)
        for field_name, field in form.fields.items():

            if isinstance(field.widget, forms.widgets.TextInput):
                # Don't overwrite any existing CSS class, append
                css_class = field.widget.attrs.get('class', u'text_field')
                field.widget.attrs['class'] = u' '.join([css_class, 'text_field'])
            elif isinstance(field.widget, forms.widgets.PasswordInput):
                # Don't overwrite any existing CSS class, append
                css_class = field.widget.attrs.get('class', u'text_field')
                field.widget.attrs['class'] = u' '.join([css_class, 'text_field'])
            elif isinstance(field.widget, forms.widgets.Textarea):
                # Don't overwrite any existing CSS class, append
                css_class = field.widget.attrs.get('class', u'text_area')
                field.widget.attrs['class'] = u' '.join([css_class, 'text_area'])

        context[self.form_name] = form
        return ''


@register.tag
def add_classes_to_form(parser, token):
    args = token.split_contents()
    return StylingNode(args[1])
