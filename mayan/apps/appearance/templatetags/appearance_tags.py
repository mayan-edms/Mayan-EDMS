from __future__ import unicode_literals

from django.template import Library
from django.utils.translation import ugettext_lazy as _

register = Library()


@register.filter
def get_choice_value(field):
    try:
        return dict(field.field.choices)[field.value()]
    except TypeError:
        return ', '.join([subwidget.data['label'] for subwidget in field.subwidgets if subwidget.data['selected']])
    except KeyError:
        return _('None')


@register.filter
def get_form_media_js(form):
    return [form.media.absolute_path(path) for path in form.media._js]


@register.simple_tag
def get_icon(icon_path):
    from django.utils.module_loading import import_string
    icon_class = import_string(icon_path)
    return icon_class.render()
    #return [form.media.absolute_path(path) for path in form.media._js]

