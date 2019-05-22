from __future__ import unicode_literals

from django.conf.urls import url

from .views import FormInstanceCreateView

urlpatterns = [
    url(
        regex=r'^templates/(?P<pk>\d+)/instances/create/$',
        view=FormInstanceCreateView.as_view(), name='form_instance_create'
    ),
]
