from __future__ import unicode_literals

from django.utils.html import format_html


def setting_widget(instance):
    return format_html(
        '<strong>{}</strong><p class="small">{}</p>', instance,
        instance.help_text or ''
    )
