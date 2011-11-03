import operator
import itertools

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.utils.simplejson import loads

from permissions.api import check_permissions, namespace_titles, get_permission_label, get_permission_namespace_label
from permissions.models import Permission
from common.utils import generate_choices_w_labels, encapsulate
from common.widgets import two_state_template

from acls import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from acls.models import AccessEntry, AccessObject, AccessHolder
from acls.widgets import object_w_content_type_icon


def _permission_titles(permission_list):
    return u', '.join([get_permission_label(permission) for permission in permission_list])
    
    
def acl_list_for(request, obj, extra_context=None):
    #check_permissions(request.user, [ACLS_VIEW_ACL])

    ct = ContentType.objects.get_for_model(obj)

    context = {
        #'app_label': ct.app_label,
        #'model_name': ct.model,
        'object_list': AccessEntry.objects.get_holders_for(obj),
        'title': _(u'access control lists for: %s' % obj),
        #'multi_select_as_buttons': True,
        #'hide_links': True,
        'extra_columns': [
            #{'name': _(u'holder'), 'attribute': 'label'},
            #{'name': _(u'obj'), 'attribute': 'holder_object'},
            #{'name': _(u'gid'), 'attribute': 'gid'},
            {'name': _(u'holder'), 'attribute': encapsulate(lambda x: object_w_content_type_icon(x.source_object))},
            {'name': _(u'permissions'), 'attribute': encapsulate(lambda x: _permission_titles(AccessEntry.objects.get_permissions_for_holder(obj, x.source_object)))},
            #{'name': _(u'arguments'), 'attribute': 'arguments'}
            ],
        #'hide_link': True,
        'hide_object': True,
        'access_object': AccessObject.encapsulate(obj)
    }

    if extra_context:
        context.update(extra_context)

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))	


def acl_list(request, app_label, model_name, object_id):
    ct = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    obj = get_object_or_404(ct.get_object_for_this_type, pk=object_id)
    return acl_list_for(request, obj)


def acl_detail(request, access_object_gid, holder_object_gid):
    #check_permissions(request.user, [ACLS_VIEW_ACL, ACLS_EDIT_ACL])
    
    try:
        holder = AccessHolder.get(gid=holder_object_gid)
        access_object = AccessObject.get(gid=access_object_gid)
    except ObjectDoesNotExist:
        raise Http404
        
    permission_list = list(set(AccessEntry.objects.get_permissions_for_holder(access_object.source_object, request.user)))
    #TODO : get all globally assigned permission, new function get_permissions_for_holder (roles aware)
    subtemplates_list = [
        {
            'name': u'generic_list_subtemplate.html',
            'context': {
                'title': _(u'permissions held by: %s for %s' % (holder, access_object)),
                'object_list': permission_list,
                'extra_columns': [
                    {'name': _(u'namespace'), 'attribute': encapsulate(lambda x: get_permission_namespace_label(x))},
                    {'name': _(u'name'), 'attribute': encapsulate(lambda x: get_permission_label(x))},
                    {
                        'name':_(u'has permission'),
                        'attribute': encapsulate(lambda x: two_state_template(AccessEntry.objects.has_accesses(x, holder.source_object, access_object.source_object)))
                    },
                ],
                #'hide_link': True,
                'hide_object': True,
            }
        },
    ]

    return render_to_response('generic_detail.html', {
        #'form': form,
        'object': access_object.obj,
        'subtemplates_list': subtemplates_list,
        'multi_select_as_buttons': True,
        'multi_select_item_properties': {
            'permission_pk': lambda x: x.pk,
            'holder_gid': lambda x: holder.gid,
            'object_gid': lambda x: access_object.gid,
            #'requester_id': lambda x: role.pk,
            #'requester_app_label': lambda x: ContentType.objects.get_for_model(role).app_label,
            #'requester_model': lambda x: ContentType.objects.get_for_model(role).model,
        },        
    }, context_instance=RequestContext(request))
    

def acl_grant(request):
    check_permissions(request.user, [ACLS_EDIT_ACL])
    items_property_list = loads(request.GET.get('items_property_list', []))
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = {}
    for item_properties in items_property_list:
        permission = get_object_or_404(Permission, pk=item_properties['permission_pk'])
        try:
            requester = AccessHolder.get(gid=item_properties['holder_gid'])
            access_object = AccessObject.get(gid=item_properties['object_gid'])
        except ObjectDoesNotExist:
            raise Http404
                
        items.setdefault(requester, {})
        items[requester].setdefault(access_object, [])
        items[requester][access_object].append(permission)
        
    title_suffix = []
    for requester, access_objects_dict in items.items():
        title_suffix.append(unicode(requester))
        for access_object, permissions in access_objects_dict.items():
            if len(permissions) == 1:
                permissions_label = _(u'permission')
            else:
                permissions_label = _(u'permissions')
            
            title_suffix.append(permission for permission in permissions)
            
               
        title_suffix.append(unicode(access_object))
        #title_suffix.append(_(u'the permissions'))
        
        
        #items = access_objects[access_object]
        #sorted_items = sorted(items, key=operator.itemgetter('requester'))
           
        # Group items by requester
        #groups = itertools.groupby(sorted_items, key=operator.itemgetter('requester'))
        #grouped_items = [(grouper, [permission['permission'] for permission in group_data]) for grouper, group_data in groups]
    
        #title_suffix
        # Warning: trial and error black magic ahead
        #title_suffix.append(_(u' and ').join([_(u'%s to %s') % (', '.join(['"%s"' % unicode(ps) for ps in p]), unicode(r)) for r, p in grouped_items]))
        
        #if len(grouped_items) == 1 and len(grouped_items[0][1]) == 1:
        #    permissions_label = _(u'permission')
        #else:
        #    permissions_label = _(u'permissions')
        #title_suffix.append(_(t

    print title_suffix
    #title_suffix = _(u' and ').join(title_suffix)
    permissions_label = _(u'permissions')

    if request.method == 'POST':
        for item in items:
            if item['permission'].grant_to(item['requester']):
                messages.success(request, _(u'Permission "%(permission)s" granted to: %(requester)s.') % {
                    'permission': item['permission'], 'requester': item['requester']})
            else:
                messages.warning(request, _(u'%(requester)s, already had the permission "%(permission)s" granted.') % {
                    'requester': item['requester'], 'permission': item['permission']})

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'key_add.png',
    }

    context['title'] = _(u'Are you sure you wish to grant the %(permissions_label)s %(title_suffix)s?') % {
        'permissions_label': permissions_label,
        'title_suffix': title_suffix,
    }
    
    if len(grouped_items) == 1:
        context['object'] = grouped_items[0][0]

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
