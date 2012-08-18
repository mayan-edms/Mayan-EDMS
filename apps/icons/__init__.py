from django.utils.translation import ugettext_lazy as _

from app_registry.models import App

try:
    app = App.register('icons', _(u'Icons'))
except App.UnableToRegister:
    pass
else:
    app.set_dependencies(['app_registry'])
