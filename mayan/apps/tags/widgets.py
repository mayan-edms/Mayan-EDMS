from django.utils.safestring import mark_safe


def get_tags_inline_widget(document):
    """
    A tag widget that includes the total tag count for a given document
    """
    # TODO: merge widgets
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
    A tag widget that displays the tags for the given document
    """
    tags_template = []

    tag_count = document.tags.count()
    if tag_count:
        tags_template.append('<ul class="tags">')
        for tag in document.tags.all():
            tags_template.append(get_single_tag_template(tag))

        tags_template.append('</ul>')

    return mark_safe(u''.join(tags_template))


def single_tag_widget(tag):
    tags_template = []
    tags_template.append('<ul class="tags">')
    tags_template.append(get_single_tag_template(tag))
    tags_template.append('</ul>')
    return mark_safe(u''.join(tags_template))


def get_single_tag_template(tag):
    return '<li style="background: %s">%s</li>' % (tag.tagproperties_set.get().get_color_code(), tag.name.replace(u' ', u'&nbsp;'))
