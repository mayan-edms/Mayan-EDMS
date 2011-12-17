from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from acls.views import acl_list_for, acl_new_holder_for
from acls.models import AccessEntry


def document_acl_list(request, document_id):
	document = get_object_or_404(Document, pk=document_id)
	return acl_list_for(
		request,
		document,
		extra_context={
			'object': document,
		}
	)


def document_new_holder(request, document_id):
	document = get_object_or_404(Document, pk=document_id)
	return acl_new_holder_for(
		request,
		document,
		extra_context={
			'object': document,
            'submit_label': _(u'Select'),
            'submit_icon_famfam': 'tick'            
		}
	)
