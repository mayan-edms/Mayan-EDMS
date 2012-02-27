from django import forms
from django.utils.translation import ugettext_lazy as _
#from django.utils.translation import ugettext
#from django.core.urlresolvers import reverse
#from django.utils.safestring import mark_safe
#from django.conf import settings


class DetachedSignatureForm(forms.Form):
    file = forms.FileField(
        label=_(u'Signature file'),
    )
