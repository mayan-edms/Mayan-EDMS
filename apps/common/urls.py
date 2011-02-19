from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings


urlpatterns = patterns('common.views',
    url(r'^about/$', direct_to_template, { 'template' : 'about.html'}, 'about'),
    url(r'^password/change/done/$', 'password_change_done', (), name='password_change_done'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login_view'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/'}, name='logout_view' ),

    url(r'^password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change_form.html', 'post_change_redirect': '/password/change/done/'}, name='password_change_view'),
    #url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_change_done.html'}),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'email_template_name' : 'password_reset_email.html', 'template_name': 'password_reset_form.html', 'post_reset_redirect' : '/password/reset/done'}, name='password_reset_view'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', { 'template_name' : 'password_reset_confirm.html', 'post_reset_redirect' : '/password/reset/complete/'}, name='password_reset_confirm_view'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', { 'template_name' : 'password_reset_complete.html' }, name='password_reset_complete_view'),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', { 'template_name' : 'password_reset_done.html'}, name='password_reset_done_view'),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%s%s' %(settings.MEDIA_URL, 'images/favicon.ico')}),
)

urlpatterns += patterns('',
    url(r'^set_language/$', 'django.views.i18n.set_language', name='set_language'),
)
