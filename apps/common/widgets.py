from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms


class PlainWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % value)


class DetailSelectMultiple(forms.widgets.SelectMultiple):
    def __init__(self, queryset=None, *args, **kwargs):
        self.queryset = queryset
        super(DetailSelectMultiple, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=(), *args, **kwargs):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        css_class = final_attrs.get('class', 'list')
        output = u'<ul class="%s">' % css_class
        options = None
        if value:
            if getattr(value, '__iter__', None):
                options = [(index, string) for index, string in \
                    self.choices if index in value]
            else:
                options = [(index, string) for index, string in \
                    self.choices if index == value]
        else:
            if self.choices:
                if self.choices[0] != (u'', u'---------') and value != []:
                    options = [(index, string) for index, string in \
                        self.choices]

        if options:
            for index, string in options:
                if self.queryset:
                    try:
                        output += u'<li><a href="%s">%s</a></li>' % (
                            self.queryset.get(pk=index).get_absolute_url(),
                            string)
                    except AttributeError:
                        output += u'<li>%s</li>' % (string)
                else:
                    output += u'<li>%s</li>' % string
        else:
            output += u'<li>%s</li>' % _(u"None")
        return mark_safe(output + u'</ul>\n')


def exists_with_famfam(path):
    try:
        return two_state_template(os.path.exists(path))
    except Exception, exc:
        return exc


def two_state_template(state, famfam_ok_icon=u'tick', famfam_fail_icon=u'cross'):
    if state:
        return mark_safe(u'<span class="famfam active famfam-%s"></span>' % famfam_ok_icon)
    else:
        return mark_safe(u'<span class="famfam active famfam-%s"></span>' % famfam_fail_icon)
