import logging
import operator
import itertools

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.utils.simplejson import loads

from permissions.models import Permission, Role
from common.utils import generate_choices_w_labels, encapsulate
from common.widgets import two_state_template

from acls import (ACLS_EDIT_ACL, ACLS_VIEW_ACL, ACLS_CLASS_EDIT_ACL,
    ACLS_CLASS_VIEW_ACL)
from acls.models import (AccessEntry, AccessObject, AccessHolder,
    DefaultAccessEntry, AccessObjectClass, ClassAccessHolder)
from acls.widgets import object_w_content_type_icon
from acls.forms import HolderSelectionForm

logger = logging.getLogger(__name__)


def _permission_titles(permission_list):
    return u', '.join([unicode(permission) for permission in permission_list])
    
    
def acl_list_for(request, obj, extra_context=None):
    Permission.objects.check_permissions(request.user, [ACLS_VIEW_ACL])

    ct = ContentType.objects.get_for_model(obj)

    context = {
        'object_list': AccessEntry.objects.get_holders_for(obj),
        'title': _(u'access control lists for: %s' % obj),
        #'multi_select_as_buttons': True,
        #'hide_links': True,
        'extra_columns': [
            {'name': _(u'holder'), 'attribute': encapsulate(lambda x: object_w_content_type_icon(x.source_object))},
            {'name': _(u'permissions'), 'attribute': encapsulate(lambda x: _permission_titles(AccessEntry.objects.get_holder_permissions_for(obj, x.source_object)))},
        ],
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
    Permission.objects.check_permissions(request.user, [ACLS_VIEW_ACL, ACLS_EDIT_ACL])
    
    try:
        holder = AccessHolder.get(gid=holder_object_gid)
        access_object = AccessObject.get(gid=access_object_gid)
    except ObjectDoesNotExist:
        raise Http404
        
    permission_list = list(access_object.get_class_permissions())
    #TODO : get all globally assigned permission, new function get_permissions_for_holder (roles aware)
    subtemplates_list = [
        {
            'name': u'generic_list_subtemplate.html',
            'context': {
                'title': _(u'permissions available to: %s for %s' % (holder, access_object)),
                'object_list': permission_list,
                'extra_columns': [
                    {'name': _(u'namespace'), 'attribute': 'namespace'},
                    {'name': _(u'label'), 'attribute': 'label'},
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
        'object': access_object.obj,
        'subtemplates_list': subtemplates_list,
        'multi_select_as_buttons': True,
        'multi_select_item_properties': {
            'permission_pk': lambda x: x.pk,
            'holder_gid': lambda x: holder.gid,
            'object_gid': lambda x: access_object.gid,
        },        
    }, context_instance=RequestContext(request))
    

def acl_grant(request):
    Permission.objects.check_permissions(request.user, [ACLS_EDIT_ACL])
    items_property_list = loads(request.GET.get('items_property_list', []))
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = {}
    title_suffix = []
    navigation_object = None
    navigation_object_count = 0

    for item_properties in items_property_list:
        try:
            permission = Permission.objects.get({'pk': item_properties['permission_pk']})
        except Permission.DoesNotExist:
            raise Http404        
        try:
            requester = AccessHolder.get(gid=item_properties['holder_gid'])
            access_object = AccessObject.get(gid=item_properties['object_gid'])
        except ObjectDoesNotExist:
            raise Http404
                
        items.setdefault(requester, {})
        items[requester].setdefault(access_object, [])
        items[requester][access_object].append(permission)
        navigation_object = access_object
        navigation_object_count += 1
        
    for requester, obj_ps in items.items():
        for obj, ps in obj_ps.items():
            title_suffix.append(_(u' and ').join([u'"%s"' % unicode(p) for p in ps]))
            title_suffix.append(_(u' for %s') % obj)
        title_suffix.append(_(u' to %s') % requester)
        
    if len(items_property_list) == 1:
        title_prefix = _(u'Are you sure you wish to grant the permission %(title_suffix)s?')
    else:
        title_prefix = _(u'Are you sure you wish to grant the permissions %(title_suffix)s?')

    if request.method == 'POST':
        for requester, object_permissions in items.items():
            for obj, permissions in object_permissions.items():
                for permission in permissions:
                    if AccessEntry.objects.grant(permission, requester.source_object,  obj.source_object):
                        messages.success(request, _(u'Permission "%(permission)s" granted to %(requester)s for %(object)s.') % {
                            'permission': permission,
                            'requester': requester,
                            'object': obj
                        })
                    else:
                        messages.warning(request, _(u'%(requester)s, already had the permission "%(permission)s" granted for %(object)s.') % {
                            'requester': requester,
                            'permission': permission,
                            'object': obj,
                        })

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'key_add.png',
    }

    context['title'] = title_prefix % {
        'title_suffix': u''.join(title_suffix),
    }
    
    logger.debug('navigation_object_count: %d' % navigation_object_count)
    logger.debug('navigation_object: %s' % navigation_object)
    if navigation_object_count == 1:
        context['object'] = navigation_object.source_object

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def acl_revoke(request):
    Permission.objects.check_permissions(request.user, [ACLS_EDIT_ACL])
    items_property_list = loads(request.GET.get('items_property_list', []))
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = {}
    title_suffix = []
    navigation_object = None
    navigation_object_count = 0

    for item_properties in items_property_list:
        try:
            permission = Permission.objects.get({'pk': item_properties['permission_pk']})
        except Permission.DoesNotExist:
            raise Http404        
        try:
            requester = AccessHolder.get(gid=item_properties['holder_gid'])
            access_object = AccessObject.get(gid=item_properties['object_gid'])
        except ObjectDoesNotExist:
            raise Http404
                
        items.setdefault(requester, {})
        items[requester].setdefault(access_object, [])
        items[requester][access_object].append(permission)
        navigation_object = access_object
        navigation_object_count += 1
        
    for requester, obj_ps in items.items():
        for obj, ps in obj_ps.items():
            title_suffix.append(_(u' and ').join([u'"%s"' % unicode(p) for p in ps]))
            title_suffix.append(_(u' for %s') % obj)
        title_suffix.append(_(u' from %s') % requester)
        
    if len(items_property_list) == 1:
        title_prefix = _(u'Are you sure you wish to revoke the permission %(title_suffix)s?')
    else:
        title_prefix = _(u'Are you sure you wish to revoke the permissions %(title_suffix)s?')

    if request.method == 'POST':
        for requester, object_permissions in items.items():
            for obj, permissions in object_permissions.items():
                for permission in permissions:
                    if AccessEntry.objects.revoke(permission, requester.source_object,  obj.source_object):
                        messages.success(request, _(u'Permission "%(permission)s" revoked of %(requester)s for %(object)s.') % {
                            'permission': permission,
                            'requester': requester,
                            'object': obj
                        })
                    else:
                        messages.warning(request, _(u'%(requester)s, didn\'t had the permission "%(permission)s" for %(object)s.') % {
                            'requester': requester,
                            'permission': permission,
                            'object': obj,
                        })

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'key_delete.png',
    }

    context['title'] = title_prefix % {
        'title_suffix': u''.join(title_suffix),
    }
    
    logger.debug('navigation_object_count: %d' % navigation_object_count)
    logger.debug('navigation_object: %s' % navigation_object)
    if navigation_object_count == 1:
        context['object'] = navigation_object.source_object

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def acl_new_holder_for(request, obj, extra_context=None):
    Permission.objects.check_permissions(request.user, [ACLS_EDIT_ACL])

    if request.method == 'POST':
        form = HolderSelectionForm(request.POST)
        if form.is_valid():
            try:
                access_object = AccessObject.encapsulate(obj)
                access_holder = AccessHolder.get(form.cleaned_data['holder_gid'])

                return HttpResponseRedirect(reverse('acl_detail', args=[access_object.gid, access_holder.gid]))
            except ObjectDoesNotExist:
                raise Http404
    else:
        form = HolderSelectionForm()

    context = {
        'form': form,
        'title': _(u'add new holder for: %s') % obj,
    }

    if extra_context:
        context.update(extra_context)
        
    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))        


# Setup views
def acl_setup_valid_classes(request):
    Permission.objects.check_permissions(request.user, [ACLS_CLASS_VIEW_ACL, ACLS_CLASS_EDIT_ACL])
    logger.debug('DefaultAccessEntry.get_classes(): %s' % DefaultAccessEntry.get_classes())

    context = {
        'object_list': DefaultAccessEntry.get_classes(),
        'title': _(u'classes'),
        'extra_columns': [
            {'name': _(u'class'), 'attribute': encapsulate(lambda x: object_w_content_type_icon(x.source_object))},
            ],
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))	


def acl_class_acl_list(request, access_object_class_gid):
    Permission.objects.check_permissions(request.user, [ACLS_CLASS_VIEW_ACL, ACLS_CLASS_EDIT_ACL])
    
    access_object_class = AccessObjectClass.get(gid=access_object_class_gid)
    context = {
        'object_list': DefaultAccessEntry.objects.get_holders_for(access_object_class.source_object),
        'title': _(u'default access control lists for class: %s') % access_object_class,
        'extra_columns': [
            {'name': _(u'holder'), 'attribute': encapsulate(lambda x: object_w_content_type_icon(x.source_object))},
            {'name': _(u'permissions'), 'attribute': encapsulate(lambda x: _permission_titles(DefaultAccessEntry.objects.get_holder_permissions_for(access_object_class.source_object, x.source_object)))},
            ],
        'hide_object': True,
        'access_object_class': access_object_class,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))	


def acls_class_acl_detail(request, access_object_class_gid, holder_object_gid):
    Permission.objects.check_permissions(request.user, [ACLS_CLASS_VIEW_ACL, ACLS_CLASS_EDIT_ACL])
    try:
        holder = AccessHolder.get(gid=holder_object_gid)
        access_object_class = AccessObjectClass.get(gid=access_object_class_gid)
    except ObjectDoesNotExist:
        raise Http404
        
    permission_list = list(access_object_class.get_class_permissions())
    #TODO : get all globally assigned permission, new function get_permissions_for_holder (roles aware)
    subtemplates_list = [
        {
            'name': u'generic_list_subtemplate.html',
            'context': {
                'title': _(u'permissions available to: %s for class %s' % (holder, access_object_class)),
                'object_list': permission_list,
                'extra_columns': [
                    {'name': _(u'namespace'), 'attribute': 'namespace'},
                    {'name': _(u'label'), 'attribute': 'label'},
                    {
                        'name':_(u'has permission'),
                        'attribute': encapsulate(lambda x: two_state_template(DefaultAccessEntry.objects.has_accesses(x, holder.source_object, access_object_class.source_object)))
                    },
                ],
                #'hide_link': True,
                'hide_object': True,
            }
        },
    ]

    return render_to_response('generic_detail.html', {
        'object': access_object_class,
        'subtemplates_list': subtemplates_list,
        'multi_select_as_buttons': True,
        'multi_select_item_properties': {
            'permission_pk': lambda x: x.pk,
            'holder_gid': lambda x: holder.gid,
            'access_object_class_gid': lambda x: access_object_class.gid,
        },        
    }, context_instance=RequestContext(request))
        

def acl_class_new_holder_for(request, access_object_class_gid):
    Permission.objects.check_permissions(request.user, [ACLS_CLASS_EDIT_ACL])
    access_object_class = AccessObjectClass.get(gid=access_object_class_gid)

    if request.method == 'POST':
        form = HolderSelectionForm(request.POST)
        if form.is_valid():
            try:
                access_holder = ClassAccessHolder.get(form.cleaned_data['holder_gid'])

                return HttpResponseRedirect(reverse('acls_class_acl_detail', args=[access_object_class.gid, access_holder.gid]))
            except ObjectDoesNotExist:
                raise Http404
    else:
        form = HolderSelectionForm(current_holders=DefaultAccessEntry.objects.get_holders_for(access_object_class))

    context = {
        'form': form,
        'title': _(u'add new holder for class: %s') % unicode(access_object_class),
        'object': access_object_class,
        'submit_label': _(u'Select'),
        'submit_icon_famfam': 'tick'            
    }
       
    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))        


def acl_class_multiple_grant(request):
    Permission.objects.check_permissions(request.user, [ACLS_CLASS_EDIT_ACL])
    items_property_list = loads(request.GET.get('items_property_list', []))
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = {}
    title_suffix = []
    navigation_object = None
    navigation_object_count = 0

    for item_properties in items_property_list:
        try:
            permission = Permission.objects.get({'pk': item_properties['permission_pk']})
        except Permission.DoesNotExist:
            raise Http404        
        try:
            requester = AccessHolder.get(gid=item_properties['holder_gid'])
            access_object_class = AccessObjectClass.get(gid=item_properties['access_object_class_gid'])
        except ObjectDoesNotExist:
            raise Http404
                
        items.setdefault(requester, {})
        items[requester].setdefault(access_object_class, [])
        items[requester][access_object_class].append(permission)
        navigation_object = access_object_class
        navigation_object_count += 1
        
    for requester, obj_ps in items.items():
        for obj, ps in obj_ps.items():
            title_suffix.append(_(u' and ').join([u'"%s"' % unicode(p) for p in ps]))
            title_suffix.append(_(u' for %s') % obj)
        title_suffix.append(_(u' to %s') % requester)
        
    if len(items_property_list) == 1:
        title_prefix = _(u'Are you sure you wish to grant the permission %(title_suffix)s?')
    else:
        title_prefix = _(u'Are you sure you wish to grant the permissions %(title_suffix)s?')

    if request.method == 'POST':
        for requester, object_permissions in items.items():
            for obj, permissions in object_permissions.items():
                for permission in permissions:
                    if DefaultAccessEntry.objects.grant(permission, requester.source_object, obj.source_object):
                        messages.success(request, _(u'Permission "%(permission)s" granted to %(requester)s for %(object)s.') % {
                            'permission': permission,
                            'requester': requester,
                            'object': obj
                        })
                    else:
                        messages.warning(request, _(u'%(requester)s, already had the permission "%(permission)s" granted for %(object)s.') % {
                            'requester': requester,
                            'permission': permission,
                            'object': obj,
                        })

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'key_add.png',
    }

    context['title'] = title_prefix % {
        'title_suffix': u''.join(title_suffix),
    }
    
    logger.debug('navigation_object_count: %d' % navigation_object_count)
    logger.debug('navigation_object: %s' % navigation_object)
    if navigation_object_count == 1:
        context['object'] = navigation_object

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def acl_class_multiple_revoke(request):
    Permission.objects.check_permissions(request.user, [ACLS_CLASS_EDIT_ACL])
    items_property_list = loads(request.GET.get('items_property_list', []))
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = {}
    title_suffix = []
    navigation_object = None
    navigation_object_count = 0

    for item_properties in items_property_list:
        try:
            permission = Permission.objects.get({'pk': item_properties['permission_pk']})
        except Permission.DoesNotExist:
            raise Http404        
        try:
            requester = AccessHolder.get(gid=item_properties['holder_gid'])
            access_object_class = AccessObjectClass.get(gid=item_properties['access_object_class_gid'])
        except ObjectDoesNotExist:
            raise Http404
                
        items.setdefault(requester, {})
        items[requester].setdefault(access_object_class, [])
        items[requester][access_object_class].append(permission)
        navigation_object = access_object_class
        navigation_object_count += 1
        
    for requester, obj_ps in items.items():
        for obj, ps in obj_ps.items():
            title_suffix.append(_(u' and ').join([u'"%s"' % unicode(p) for p in ps]))
            title_suffix.append(_(u' for %s') % obj)
        title_suffix.append(_(u' from %s') % requester)
        
    if len(items_property_list) == 1:
        title_prefix = _(u'Are you sure you wish to revoke the permission %(title_suffix)s?')
    else:
        title_prefix = _(u'Are you sure you wish to revoke the permissions %(title_suffix)s?')

    if request.method == 'POST':
        for requester, object_permissions in items.items():
            for obj, permissions in object_permissions.items():
                for permission in permissions:
                    if DefaultAccessEntry.objects.revoke(permission, requester.source_object,  obj.source_object):
                        messages.success(request, _(u'Permission "%(permission)s" revoked of %(requester)s for %(object)s.') % {
                            'permission': permission,
                            'requester': requester,
                            'object': obj
                        })
                    else:
                        messages.warning(request, _(u'%(requester)s, didn\'t had the permission "%(permission)s" for %(object)s.') % {
                            'requester': requester,
                            'permission': permission,
                            'object': obj,
                        })

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'key_delete.png',
    }

    context['title'] = title_prefix % {
        'title_suffix': u''.join(title_suffix),
    }
    
    logger.debug('navigation_object_count: %d' % navigation_object_count)
    logger.debug('navigation_object: %s' % navigation_object)
    if navigation_object_count == 1:
        context['object'] = navigation_object

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
