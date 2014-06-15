from django.utils.safestring import mark_safe


def history_entry_object_link(entry):
    return mark_safe(u'<a href="%(url)s">%(label)s</a>' % {
            'url': entry.content_object.get_absolute_url() if entry.content_object else u'#',
            'label': unicode(entry.content_object) if entry.content_object else u''
        }
    )


def history_entry_summary(entry):
    return mark_safe(u'<a href="%(url)s">%(label)s</a>' % {
        'url': entry.get_absolute_url(),
        'label': unicode(entry.get_processed_summary())
    })


def history_entry_type_link(entry):
    return mark_safe(u'<a href="%(url)s">%(label)s</a>' % {
            'url': entry.history_type.get_absolute_url(),
            'label': unicode(entry.history_type)
        }
    )
