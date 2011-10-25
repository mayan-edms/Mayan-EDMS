from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group

from permissions.api import check_permissions, namespace_titles, get_permission_label
from common.utils import generate_choices_w_labels, encapsulate

from acls import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from acls.models import AccessEntry


def _permission_titles(permission_list):
	return u', '.join([get_permission_label(permission) for permission in permission_list])
	
	
def acl_list_for(request, obj, extra_context=None):
	check_permissions(request.user, [ACLS_VIEW_ACL])

	context = {
		'object_list': AccessEntry.objects.get_holders_for(obj),
		'title': _(u'access control lists for: %s' % obj),
		#'multi_select_as_buttons': True,
		#'hide_links': True,
		'extra_columns': [
			#{'name': _(u'holder'), 'attribute': 'label'},
			{'name': _(u'holder'), 'attribute': 'widget'},
			{'name': _(u'permissions'), 'attribute': encapsulate(lambda x: _permission_titles(AccessEntry.objects.get_acls_for_holder(obj, x['object'])))},
			#{'name': _(u'arguments'), 'attribute': 'arguments'}
			],
		#'hide_link': True,
		'hide_object': True,
	}

	if extra_context:
		context.update(extra_context)

	return render_to_response('generic_list.html', context,
		context_instance=RequestContext(request))	


def acl_list(request, app_label, model_name, object_id):
	ct = get_object_or_404(ContentType, app_label=app_label, model=model_name)
	obj = get_object_or_404(ContentType.user_type.get_object_for_this_type, pk=object_id)
	return acl_list_for(request, obj)


