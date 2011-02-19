from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from models import Role, Permission, PermissionHolder
from forms import RoleForm, RoleForm_view
from permissions import PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT, \
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, PERMISSION_PERMISSION_GRANT, \
    PERMISSION_PERMISSION_REVOKE
from api import check_permissions, Unauthorized


def role_list(request):
    permissions = [PERMISSION_ROLE_VIEW]
    try:
        check_permissions(request.user, 'permissions', permissions)
    except Unauthorized, e:
        raise Http404(e)
            
    return object_list(
        request,
        queryset=Role.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title':_(u'roles'),
            'hide_link':True,
        },
    )


def _role_permission_link(requester, permission, permission_list):
    ct = ContentType.objects.get_for_model(requester)

    template = '<a href="%(url)s"><span class="famfam active famfam-%(icon)s"></span>%(text)s</a>'

    if permission in permission_list:
        return template % {
            'url':reverse('permission_revoke',
                args=[permission.id, ct.app_label, ct.model, requester.id]),
            'icon':'delete', 'text':_(u'Revoke')}
    else:
        return template % {
            'url':reverse('permission_grant',
                args=[permission.id, ct.app_label, ct.model, requester.id]),
            'icon':'add', 'text':_(u'Grant')}
        
        
def role_permissions(request, role_id):
    permissions = [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE]
    try:
        check_permissions(request.user, 'permissions', permissions)
    except Unauthorized, e:
        raise Http404(e)
            
    role = get_object_or_404(Role, pk=role_id)
    form = RoleForm_view(instance=role)

    role_permissions = Permission.objects.get_for_holder(role)
    subtemplates_dict = [
        {
            'name':'generic_list_subtemplate.html',
            'title':_(u'permissions'),
            'object_list':Permission.objects.all(),
            'extra_columns':[
                {'name':_(u'namespace'), 'attribute':'namespace'},
                {'name':_(u'name'), 'attribute':'label'},
                {'name':_(u'state'), 'attribute':lambda x: _role_permission_link(role, x, role_permissions)}
            ],
            'hide_link':True,
            'hide_object':True,
        },
    ]
           
    return render_to_response('generic_detail.html', {
        'form':form,
        'object':role,
        'object_name':_(u'role'),
        'subtemplates_dict':subtemplates_dict,
    }, context_instance=RequestContext(request))


def role_edit(request, role_id):
    permissions = [PERMISSION_ROLE_EDIT]
    try:
        check_permissions(request.user, 'permissions', permissions)
    except Unauthorized, e:
        raise Http404(e)

    return update_object(request, template_name='generic_form.html', 
        form_class=RoleForm, object_id=role_id, extra_context={
        'object_name':_(u'role')})


def role_create(request):
    permissions = [PERMISSION_ROLE_CREATE]
    try:
        check_permissions(request.user, 'permissions', permissions)
    except Unauthorized, e:
        raise Http404(e)

    return create_object(request, model=Role, 
        template_name='generic_form.html',
        post_save_redirect=reverse('role_list'))

    
def role_delete(request, role_id):
    permissions = [PERMISSION_ROLE_DELETE]
    try:
        check_permissions(request.user, 'permissions', permissions)
    except Unauthorized, e:
        raise Http404(e)
            
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
        
    return delete_object(request, model=Role, object_id=role_id, 
        template_name='generic_confirm.html', 
        post_delete_redirect=reverse('role_list'),
        extra_context={
            'delete_view':True,
            'next':next,
            'previous':previous,
            'object_name':_(u'role'),
        })

def permission_grant_revoke(request, permission_id, app_label, module_name, pk, action):
    ct = get_object_or_404(ContentType, app_label=app_label, model=module_name)
    requester_model = ct.model_class()
    requester = get_object_or_404(requester_model, pk=pk)
    permission = get_object_or_404(Permission, pk=permission_id)

    if action == 'grant':
        permissions = [PERMISSION_PERMISSION_GRANT]
        try:
            check_permissions(request.user, 'permissions', permissions)
        except Unauthorized, e:
            raise Http404(e)
        title = _('Are you sure you wish to grant the permission "%s" to %s: %s') % (permission, ct.name, requester)

    elif action == 'revoke':
        permissions = [PERMISSION_PERMISSION_REVOKE]
        try:
            check_permissions(request.user, 'permissions', permissions)
        except Unauthorized, e:
            raise Http404(e)
        title = _('Are you sure you wish to revoke the permission "%s" from %s: %s') % (permission, ct.name, requester)
    else:
        return HttpResponseRedirect('/')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))


    if request.method == 'POST':
        if action == 'grant':
            permission_holder, created = PermissionHolder.objects.get_or_create(permission=permission, holder_type=ct, holder_id=requester.id)
            if created:
                messages.success(request, _(u'Permission "%s" granted to %s: %s.') % (permission, ct.name, requester))
            else:
                messages.warning(request, _(u'%s: %s, already had the permission "%s" granted.') % (ct.name, requester, permission))
        elif action == 'revoke':
            try:
                permission_holder = PermissionHolder.objects.get(permission=permission, holder_type=ct, holder_id=requester.id)
                permission_holder.delete()
                messages.success(request, _(u'Permission "%s" revoked from %s: %s.') % (permission, ct.name, requester))
            except ObjectDoesNotExist:
                messages.warning(request, _(u'%s: %s doesn\'t have the permission "%s".') % (ct.name, requester, permission))
        return HttpResponseRedirect(next)
        
    return render_to_response('generic_confirm.html', {
        'object':requester,
        'next':next,
        'previous':previous,
        'title':title,
    }, context_instance=RequestContext(request))


