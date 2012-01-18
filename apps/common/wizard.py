"""Common abstract classes for forms."""
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django import forms
from django.conf import settings
from django.contrib.formtools.wizard import FormWizard
from django.forms.forms import BoundField
from django.forms.formsets import BaseFormSet
from django.utils.hashcompat import md5_constructor

__all__ = ('security_hash', 'BoundFormWizard')


def security_hash_new(form, exclude=None, *args):
    """
    Calculates a security hash for the given Form/FormSet instance.

    This creates a list of the form field names/values in a deterministic
    order, pickles the result with the SECRET_KEY setting, then takes an md5
    hash of that.
    """

    data = []
    if exclude is None:
        exclude = ()
    if isinstance(form, BaseFormSet):
        for _form in form.forms + [form.management_form]:
            for bf in _form:
                value = bf.field.clean(bf.data) or ''
                if isinstance(value, basestring):
                    value = value.strip()
                data.append((bf.name, value))
    else:
        for bf in form:
            if bf.name in exclude:
                continue
            value = bf.field.clean(bf.data) or ''
            if isinstance(value, basestring):
                value = value.strip()
            data.append((bf.name, value))
    data.extend(args)
    data.append(settings.SECRET_KEY)

    # Use HIGHEST_PROTOCOL because it's the most efficient. It requires
    # Python 2.3, but Django requires 2.3 anyway, so that's OK.
    pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

    return md5_constructor(pickled).hexdigest()


class BoundFormWizard(FormWizard):
    """
    Render prev_fields as a list of bound form fields in the template
    context rather than raw html.
    """

    def security_hash(self, request, form):
        """
        Calculates the security hash for the given HttpRequest and
        Form/FormSet instances.

        Subclasses may want to take into account request-specific information,
        such as the IP address.
        """

        return security_hash_new(form)

    def render(self, form, request, step, context=None):
        'Renders the given Form object, returning an HttpResponse.'
        old_data = request.POST
        prev_fields = []
        if old_data:
            for i in range(step):
                old_form = self.get_form(i, old_data)
                hash_name = 'hash_%s' % i
                if isinstance(old_form, BaseFormSet):
                    for _form in old_form.forms + [old_form.management_form]:
                        prev_fields.extend([bf for bf in _form])
                else:
                    prev_fields.extend([bf for bf in old_form])
                hash_field = forms.Field(initial=old_data.get(hash_name,
                    self.security_hash(request, old_form)))
                bf = BoundField(forms.Form(), hash_field, hash_name)
                prev_fields.append(bf)
        return self.render_template(request, form, prev_fields, step, context)
