from django.utils.translation import ugettext_lazy as _


def get_tags_inline_widget(document):
    tags_template = []
    tag_block_template = u'<div style="padding: 0px 5px 0px 5px; border: 1px solid black; background: %s;">%s</div>'
    tag_count = document.tags.count()
    if tag_count:
        tags_template.append(u'<div class="tc">')
        tags_template.append(u'<div>%(tag_string)s: %(tag_count)s</div>' % {
            'tag_string': _(u'Tags'), 'tag_count': tag_count})
        
        for tag in document.tags.all():
            tags_template.append(tag_block_template % (tag.tagproperties_set.get().get_color_code(), tag.name))

        tags_template.append(u'</div>')
    return u''.join(tags_template)


def get_tags_inline_widget_simple(document):
    tags_template = []
    tag_block_template = u'<div style="padding: 0px 5px 0px 5px; border: 1px solid black; background: %s;">%s</div>'
    tag_count = document.tags.count()
    if tag_count:
        tags_template.append(u'<div class="tc">')
        
        for tag in document.tags.all():
            tags_template.append(tag_block_template % (tag.tagproperties_set.get().get_color_code(), tag.name))

        tags_template.append(u'</div>')
    return u''.join(tags_template)
