from django.conf.urls import url

from .views import (
    CurrentUserLocaleProfileDetailsView, CurrentUserLocaleProfileEditView
)

urlpatterns = [
    url(
        regex=r'^user/locale/$', name='current_user_locale_profile_details',
        view=CurrentUserLocaleProfileDetailsView.as_view()
    ),
    url(
        regex=r'^user/locale/edit/$', name='current_user_locale_profile_edit',
        view=CurrentUserLocaleProfileEditView.as_view()
    )
]
