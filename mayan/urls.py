from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('main.urls', namespace='main')),
    url(r'^accounts/', include('user_management.urls', namespace='user_management')),
    url(r'^acls/', include('acls.urls', namespace='acls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('rest_api.urls')),
    url(r'^checkouts/', include('checkouts.urls', namespace='checkouts')),
    url(r'^comments/', include('document_comments.urls', namespace='comments')),
    url(r'^common/', include('common.urls', namespace='common')),
    url(r'^document/acls/', include('document_acls.urls', namespace='document_acls')),
    url(r'^document/signatures/', include('document_signatures.urls', namespace='signatures')),
    url(r'^document/states/', include('document_states.urls', namespace='document_states')),
    url(r'^documents/', include('documents.urls', namespace='documents')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^folders/', include('folders.urls', namespace='folders')),
    url(r'^gpg/', include('django_gpg.urls', namespace='django_gpg')),
    url(r'^indexing/', include('document_indexing.urls', namespace='indexing')),
    url(r'^installation/', include('installation.urls', namespace='installation')),
    url(r'^linking/', include('linking.urls', namespace='linking')),
    url(r'^mailer/', include('mailer.urls', namespace='mailer')),
    url(r'^metadata/', include('metadata.urls', namespace='metadata')),
    url(r'^ocr/', include('ocr.urls', namespace='ocr')),
    url(r'^permissions/', include('permissions.urls', namespace='permissions')),
    url(r'^registration/', include('registration.urls', namespace='registration')),
    url(r'^search/', include('dynamic_search.urls', namespace='search')),
    url(r'^settings/', include('smart_settings.urls', namespace='settings')),
    url(r'^setup/', include('project_setup.urls', namespace='project_setup')),
    url(r'^sources/', include('sources.urls', namespace='sources')),
    url(r'^statistics/', include('statistics.urls', namespace='statistics')),
    url(r'^tags/', include('tags.urls', namespace='tags')),
    url(r'^tools/', include('project_tools.urls', namespace='project_tools')),
)


def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns(
            '',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'))

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += patterns(
            '',
            url(r'^__debug__/', include(debug_toolbar.urls)))
