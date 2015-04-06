from __future__ import unicode_literals

from django.utils.html import escape
from django.utils.safestring import mark_safe


def get_tags_inline_widget_simple(document):
    """
    A tag widget that displays the tags for the given document
    """
    tags_template = []

    tag_count = document.tags.count()
    if tag_count:
        for tag in document.tags.all():
            tags_template.append(get_single_tag_template(tag))

    return mark_safe(''.join(tags_template))


def single_tag_widget(tag):
    tags_template = []
    tags_template.append(get_single_tag_template(tag))
    return mark_safe(''.join(tags_template))


def get_single_tag_template(tag):
    return '<span class="label label-tag" style="background: %s">%s</span>' % (tag.get_color_code(), escape(tag.label).replace(' ', '&nbsp;'))
