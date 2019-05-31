from __future__ import unicode_literals

from django.conf.urls import url

from .views import FormInstanceCreateView, FormInstanceEditView

urlpatterns = [
    url(
        regex=r'^templates/(?P<pk>\d+)/instances/create/$',
        view=FormInstanceCreateView.as_view(), name='form_instance_create'
    ),
    url(
        regex=r'^instances/(?P<pk>\d+)/edit/$',
        view=FormInstanceEditView.as_view(), name='form_instance_edit'
    ),
]
