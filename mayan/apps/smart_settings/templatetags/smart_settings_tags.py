from django.template import Library

from ..classes import Setting

register = Library()


@register.simple_tag
def smart_setting(global_name):
    return Setting.get(global_name=global_name).value


@register.simple_tag
def smart_settings_check_changed():
    return Setting.check_changed()
