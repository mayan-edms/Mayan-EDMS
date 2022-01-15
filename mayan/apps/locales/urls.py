from django.conf.urls import url

from .views import UserLocaleProfileDetailView, UserLocaleProfileEditView

urlpatterns = [
    url(
        regex=r'^user/(?P<user_id>\d+)/locale/$',
        name='user_locale_profile_detail',
        view=UserLocaleProfileDetailView.as_view()
    ),
    url(
        regex=r'^user/(?P<user_id>\d+)/locale/edit/$',
        name='user_locale_profile_edit',
        view=UserLocaleProfileEditView.as_view()
    )
]
