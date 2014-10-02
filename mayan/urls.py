from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^', include('common.urls', namespace='common')),
    (r'^', include('main.urls', namespace='main')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    (r'^documents/', include('documents.urls', namespace='documents')),
    (r'^folders/', include('folders.urls', namespace='folders')),
    (r'^search/', include('dynamic_search.urls', namespace='search')),
    (r'^ocr/', include('ocr.urls', namespace='ocr')),
    (r'^permissions/', include('permissions.urls', namespace='permissions')),
    (r'^tags/', include('tags.urls', namespace='tags')),
    (r'^comments/', include('document_comments.urls', namespace='comments')),
    (r'^user_management/', include('user_management.urls', namespace='user_management')),
    (r'^settings/', include('smart_settings.urls', namespace='settings')),
    (r'^metadata/', include('metadata.urls', namespace='metadata')),
    (r'^linking/', include('linking.urls', namespace='linking')),
    (r'^document_indexing/', include('document_indexing.urls', namespace='indexing')),
    (r'^history/', include('history.urls', namespace='history')),
    (r'^sources/', include('sources.urls', namespace='sources')),
    (r'^project_setup/', include('project_setup.urls', namespace='project_setup')),
    (r'^project_tools/', include('project_tools.urls', namespace='project_tools')),
    (r'^acls/', include('acls.urls', namespace='acls')),
    (r'^document_acls/', include('document_acls.urls', namespace='document_acls')),
    (r'^api/', include('rest_api.urls')),
    (r'^gpg/', include('django_gpg.urls', namespace='django_gpg')),
    (r'^documents/signatures/', include('document_signatures.urls', namespace='signatures')),
    (r'^checkouts/', include('checkouts.urls', namespace='checkout')),
    (r'^installation/', include('installation.urls', namespace='installation')),
    (r'^scheduler/', include('scheduler.urls', namespace='scheduler')),
    (r'^bootstrap/', include('bootstrap.urls', namespace='bootstrap')),
    (r'^registration/', include('registration.urls', namespace='registration')),
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
