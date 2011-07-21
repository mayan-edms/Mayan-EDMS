from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class FamFamRadioFieldRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        results = []
        results.append(u'<ul>\n')
        for w in self:
            if w.choice_value:
                famfam_template = u'<span class="famfam active famfam-%s" style="vertical-align: bottom;"></span>' % w.choice_value
            else:
                famfam_template = u'<span class="famfam active famfam-cross" style="vertical-align: bottom;"></span>'
            results.append(u'<li class="undecorated_list">%s%s</li>' % (famfam_template, force_unicode(w)))
        
        results.append(u'\n</ul>')
        return mark_safe(u'\n'.join(results))


class FamFamRadioSelect(forms.widgets.RadioSelect):
    renderer = FamFamRadioFieldRenderer
