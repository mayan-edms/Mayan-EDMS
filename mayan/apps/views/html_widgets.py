from django.template.loader import render_to_string
from django.utils.encoding import force_text

from mayan.apps.templating.classes import Template

from .icons import icon_fail as default_icon_fail
from .icons import icon_ok as default_icon_ok


class TwoStateWidget:
    template_name = 'common/two_state_widget.html'

    def __init__(self, center=False, icon_ok=None, icon_fail=None):
        self.icon_ok = icon_ok or default_icon_ok
        self.icon_fail = icon_fail or default_icon_fail

    def render(self, name=None, value=None):
        return render_to_string(
            template_name=self.template_name, context={
                'icon_ok': self.icon_ok, 'icon_fail': self.icon_fail,
                'value': value
            }
        )


class ObjectLinkWidget:
    template_string = '<a href="{{ url }}">{{ object_type }}{{ label }}</a>'

    def __init__(self):
        self.template = Template(template_string=self.template_string)

    def render(self, name=None, value=None):
        label = ''
        object_type = ''
        url = None

        if value:
            label = force_text(s=value)
            object_type = '{}: '.format(value._meta.verbose_name)
            try:
                url = value.get_absolute_url()
            except AttributeError:
                url = None

            if getattr(value, 'is_staff', None) or getattr(value, 'is_superuser', None):
                # Don't display a anchor to for the user details view for
                # superusers and staff, the details view filters them. Staff
                # and admin users are not manageable by the normal user views.
                url = '#'
                return '{}{}'.format(object_type, label)

        return self.template.render(
            context={
                'label': label, 'object_type': object_type,
                'url': url or '#'
            }
        )
