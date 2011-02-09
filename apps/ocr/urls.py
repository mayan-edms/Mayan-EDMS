from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('ocr.views',
    url(r'^(?P<document_id>\d+)/submit/$', 'submit_document', (), 'submit_document'),
)
