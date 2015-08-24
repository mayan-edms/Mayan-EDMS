from __future__ import unicode_literals

from django.utils.html import escape
from django.utils.safestring import mark_safe


def widget_inline_tags(document):
    """
    A tag widget that displays the tags for the given document
    """
    tags_template = []

    tag_count = document.tags().count()
    if tag_count:
        for tag in document.tags().all():
            tags_template.append(widget_single_tag(tag))

    return mark_safe(''.join(tags_template))


def widget_single_tag(tag):
    return mark_safe(
        '''
            <span class="label label-tag" style="background: {}">{}</span>
        '''.format(tag.color, escape(tag.label).replace(' ', '&nbsp;'))
    )
