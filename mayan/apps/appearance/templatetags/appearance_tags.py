import bleach

from django.apps import apps
from django.conf import settings
from django.template import Library
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

app_templates_cache = {}
register = Library()


@register.simple_tag
def appearance_app_templates(template_name):
    result = []

    for app in apps.get_app_configs():
        template_id = '{}.{}'.format(app.label, template_name)

        if settings.DEBUG or template_id not in app_templates_cache:
            try:
                app_templates_cache[template_id] = get_template(
                    '{}/app/{}.html'.format(app.label, template_name)
                ).render()
            except TemplateDoesNotExist:
                """Non fatal"""
                app_templates_cache[template_id] = ''

        result.append(app_templates_cache[template_id])

    return mark_safe('\n'.join(result))


@register.filter
def appearance_get_choice_value(field):
    try:
        return dict(field.field.choices)[field.value()]
    except TypeError:
        return ', '.join([subwidget.data['label'] for subwidget in field.subwidgets if subwidget.data['selected']])
    except KeyError:
        return _('None')


@register.filter
def appearance_get_form_media_js(form):
    return [form.media.absolute_path(path) for path in form.media._js]


@register.simple_tag
def appearance_get_icon(icon_path):
    return import_string(dotted_path=icon_path).render()


@register.simple_tag
def appearance_get_user_theme_stylesheet(user):
    if user and user.is_authenticated:
        theme = user.theme_settings.theme

        if theme:
            return bleach.clean(
                text=user.theme_settings.theme.stylesheet,
                tags=('style',)
            )

    return ''


@register.simple_tag
def appearance_icon_render(icon_class, enable_shadow=False):
    return icon_class.render(extra_context={'enable_shadow': enable_shadow})


@register.filter
def appearance_object_list_count(object_list):
    try:
        return object_list.count()
    except TypeError:
        return len(object_list)
