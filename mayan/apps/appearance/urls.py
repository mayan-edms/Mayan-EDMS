from django.conf.urls import url

from mayan.apps.views.generics import SimpleView

urlpatterns = [
    url(
        regex=r'^errors/403/$', name='error_403', view=SimpleView.as_view(
            template_name='403.html'
        )
    ),
    url(
        regex=r'^errors/404/$', name='error_404', view=SimpleView.as_view(
            template_name='404.html'
        )
    ),
    url(
        regex=r'^errors/500/$', name='error_500', view=SimpleView.as_view(
            template_name='500.html'
        )
    ),
]
