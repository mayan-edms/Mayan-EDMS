from mayan.apps.views.forms import DetailForm

from .models import Cache


class CacheDetailForm(DetailForm):
    class Meta:
        fields = ()
        model = Cache
