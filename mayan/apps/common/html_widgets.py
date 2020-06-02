from django.template.loader import render_to_string

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
