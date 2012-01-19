from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


def get_tags_inline_widget(document):
    """
    A tag widget that includes the total tag count for a given document
    """
    tags_template = []
    tag_count = document.tags.count()
    if tag_count:
        tags_template.append(u'<div class="tc">')

        for tag in document.tags.all():
            tags_template.append(u'<ul class="tags"><li style="background: %s;">%s</li></ul>' % (tag.tagproperties_set.get().get_color_code(), tag.name))

        tags_template.append(u'<div style="clear:both;"></div>')
        tags_template.append(u'</div>')
    return mark_safe(u''.join(tags_template))


def get_tags_inline_widget_simple(document):
    """
    A tag widget that only displayes the rectangular colored boxes for a
    given document
    """
    tags_template = []

    tag_count = document.tags.count()
    if tag_count:
        tags_template.append('<ul class="tags">')
        for tag in document.tags.all():
            tags_template.append('<li style="background: %s">%s</li>' % (tag.tagproperties_set.get().get_color_code(), tag.name))

        tags_template.append('</ul>')

    return mark_safe(u''.join(tags_template))


def tag_color_block(tag):
    return mark_safe(u'<div style="width: 20px; height: 20px; border: 1px solid black; background: %s;"></div>' % tag.tagproperties_set.get().get_color_code())
