from django.conf.urls import url

from mayan.apps.views.generics import SimpleView

from .views import (
    ThemeCreateView, ThemeDeleteView, ThemeEditView, ThemeListView,
    UserThemeSettingsDetailsView, UserThemeSettingsEditView
)


urlpatterns_error_pages = [
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

urlpatterns_themes = [
    url(
        regex=r'^themes/$', name='theme_list',
        view=ThemeListView.as_view()
    ),
    url(
        regex=r'^themes/create/$', name='theme_create',
        view=ThemeCreateView.as_view()
    ),
    url(
        regex=r'^themes/(?P<theme_id>\d+)/delete/$',
        name='theme_delete', view=ThemeDeleteView.as_view()
    ),
    url(
        regex=r'^themes/(?P<theme_id>\d+)/edit/$', name='theme_edit',
        view=ThemeEditView.as_view()
    )
]

urlpatterns_user_theme_settings = [
    url(
        regex=r'^user/(?P<user_id>\d+)/theme/$',
        name='user_theme_settings_detail',
        view=UserThemeSettingsDetailsView.as_view()
    ),
    url(
        regex=r'^user/(?P<user_id>\d+)/theme/edit/$',
        name='user_theme_settings_edit',
        view=UserThemeSettingsEditView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_error_pages)
urlpatterns.extend(urlpatterns_themes)
urlpatterns.extend(urlpatterns_user_theme_settings)
