from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.defaults import page_not_found, server_error

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('common.urls')),
    (r'^', include('main.urls')),
    (r'^documents/', include('documents.urls')),
    (r'^filesystem_serving/', include('filesystem_serving.urls')),
    (r'^search/', include('dynamic_search.urls')),
    (r'^ocr/', include('ocr.urls')),
    (r'^permissions/', include('permissions.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^sentry/', include('sentry.urls')),
)

def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))
    
if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^%s-site_media/(?P<path>.*)$' % settings.PROJECT_NAME,
            'django.views.static.serve',
            {'document_root':'site_media', 'show_indexes':True}),
    )

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'),
        )


