from __future__ import absolute_import

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.exceptions import PermissionDenied

#from documents.permissions import (PERMISSION_DOCUMENT_CREATE,
#    PERMISSION_DOCUMENT_NEW_VERSION)
#from documents.models import DocumentType, Document
#from documents.conf.settings import THUMBNAIL_SIZE
#from metadata.api import decode_metadata_from_url, metadata_repr_as_list
from permissions.models import Permission
#from common.utils import encapsulate
#from common.widgets import two_state_template
#import sendfile
#from acls.models import AccessEntry

from .models import Workflow
#from .literals import (SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_STAGING,
#    SOURCE_CHOICE_WATCH, SOURCE_CHOICE_POP3_EMAIL, SOURCE_CHOICE_IMAP_EMAIL)
#from .literals import (SOURCE_UNCOMPRESS_CHOICE_Y,
#    SOURCE_UNCOMPRESS_CHOICE_ASK)
#from .staging import create_staging_file_class
#from .forms import (StagingDocumentForm, WebFormForm,
#    WatchFolderSetupForm)
from .permissions import PERMISSION_WORKFLOW_SETUP_VIEW


logger = logging.getLogger(__name__)


# Setup views
def setup_workflow_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_VIEW])

    context = {
        'object_list': Workflow.objects.all(),
        'title': _(u'workflows'),
        #'hide_link': True,
        #'list_object_variable_name': 'source',
        #'source_type': source_type,
        #'extra_columns': [
        #    {'name': _(u'Enabled'), 'attribute': encapsulate(lambda source: two_state_template(source.enabled))},
        #],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
