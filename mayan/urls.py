from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^', include('common.urls')),
    (r'^', include('main.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    (r'^documents/', include('documents.urls')),
    (r'^folders/', include('folders.urls')),
    (r'^search/', include('dynamic_search.urls')),
    (r'^ocr/', include('ocr.urls')),
    (r'^permissions/', include('permissions.urls')),
    (r'^tags/', include('tags.urls')),
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
    (r'^checkouts/', include('checkouts.urls')),
    (r'^installation/', include('installation.urls')),
    (r'^scheduler/', include('scheduler.urls')),
    (r'^bootstrap/', include('bootstrap.urls')),
    (r'^registration/', include('registration.urls')),
    (r'^statistics/', include('statistics.urls', namespace='statistics')),
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
