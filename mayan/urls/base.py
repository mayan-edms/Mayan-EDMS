from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

__all__ = ('urlpatterns',)

admin.autodiscover()

urlpatterns = [
    url(regex=r'^admin/', view=admin.site.urls),
]
