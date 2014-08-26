from django.conf.urls import patterns, url

from .views import EditorView

urlpatterns = patterns('',
    url(r'^$', EditorView.as_view(), name='editor_view'),
)
