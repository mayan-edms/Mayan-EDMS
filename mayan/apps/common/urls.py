from django.conf.urls import url
from django.contrib import admin

from django.views.i18n import JavaScriptCatalog

from .api_views import (
    APIContentTypeList, APITemplateDetailView, APITemplateListView
)
from .views import (
    AboutView, CurrentUserLocaleProfileDetailsView,
    CurrentUserLocaleProfileEditView, FaviconRedirectView, HomeView,
    LicenseView, RootView, SetupListView, ToolsListView
)

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

urlpatterns.extend(urlpatterns_misc)
urlpatterns.extend(urlpatterns_user_locale)

passthru_urlpatterns = [
    url(regex=r'^admin/', view=admin.site.urls),
]

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
