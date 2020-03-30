from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from .api_views import (
    APIContentTypeList, APITemplateDetailView, APITemplateListView
)
from .views import (
    AboutView, CurrentUserLocaleProfileDetailsView,
    CurrentUserLocaleProfileEditView, FaviconRedirectView, HomeView,
    LicenseView, ObjectErrorLogEntryListClearView, ObjectErrorLogEntryListView,
    RootView, SetupListView, ToolsListView
)

urlpatterns_error_logs = [
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/errors/$',
        name='object_error_list', view=ObjectErrorLogEntryListView.as_view()
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/errors/clear/$',
        name='object_error_list_clear',
        view=ObjectErrorLogEntryListClearView.as_view()
    )
]

urlpatterns_user_locale = [
    url(
        regex=r'^user/locale/$', name='current_user_locale_profile_details',
        view=CurrentUserLocaleProfileDetailsView.as_view()
    ),
    url(
        regex=r'^user/locale/edit/$', name='current_user_locale_profile_edit',
        view=CurrentUserLocaleProfileEditView.as_view()
    )
]

urlpatterns_misc = [
    url(
        regex=r'^favicon\.ico$', view=FaviconRedirectView.as_view()
    ),
    url(
        regex=r'^jsi18n/(?P<packages>\S+?)/$', name='javascript_catalog',
        view=JavaScriptCatalog.as_view()
    )
]

urlpatterns = [
    url(regex=r'^$', name='root', view=RootView.as_view()),
    url(regex=r'^home/$', name='home', view=HomeView.as_view()),
    url(regex=r'^about/$', name='about_view', view=AboutView.as_view()),
    url(regex=r'^license/$', name='license_view', view=LicenseView.as_view()),
    url(regex=r'^setup/$', name='setup_list', view=SetupListView.as_view()),
    url(regex=r'^tools/$', name='tools_list', view=ToolsListView.as_view())
]

urlpatterns.extend(urlpatterns_error_logs)
urlpatterns.extend(urlpatterns_misc)
urlpatterns.extend(urlpatterns_user_locale)

api_urls = [
    url(
        regex=r'^content_types/$', view=APIContentTypeList.as_view(),
        name='content-type-list'
    ),
    url(
        regex=r'^templates/$', view=APITemplateListView.as_view(),
        name='template-list'
    ),
    url(
        regex=r'^templates/(?P<name>[-\w]+)/$',
        view=APITemplateDetailView.as_view(), name='template-detail'
    )
]
