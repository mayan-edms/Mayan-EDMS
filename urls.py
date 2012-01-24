from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('common.urls')),
    (r'^', include('main.urls')),
    (r'^documents/', include('documents.urls')),
    (r'^folders/', include('folders.urls')),
    (r'^search/', include('dynamic_search.urls')),
    (r'^ocr/', include('ocr.urls')),
    (r'^permissions/', include('permissions.urls')),
    (r'^tags/', include('tags.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('document_comments.urls')),
    (r'^user_management/', include('user_management.urls')),
    (r'^settings/', include('smart_settings.urls')),
    (r'^metadata/', include('metadata.urls')),
    (r'^linking/', include('linking.urls')),
    (r'^document_indexing/', include('document_indexing.urls')),
    (r'^history/', include('history.urls')),
    (r'^converter/', include('converter.urls')),
    (r'^sources/', include('sources.urls')),
    (r'^project_setup/', include('project_setup.urls')),
    (r'^project_tools/', include('project_tools.urls')),
    (r'^acls/', include('acls.urls')),
    (r'^document_acls/', include('document_acls.urls')),
    (r'^api/', include('rest_api.urls')),
    (r'^gpg/', include('django_gpg.urls')),
    (r'^documents/signatures/', include('document_signatures.urls')),
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

if settings.DEVELOPMENT:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'),
        )
