import operator
import itertools

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
from django.utils.simplejson import loads

from common.views import assign_remove
from common.utils import generate_choices_w_labels, encapsulate
from common.widgets import two_state_template

from permissions.models import Role, Permission, PermissionHolder, RoleMember
from permissions.forms import RoleForm, RoleForm_view
from permissions import PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT, \
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, PERMISSION_PERMISSION_GRANT, \
    PERMISSION_PERMISSION_REVOKE
from permissions.api import check_permissions, namespace_titles
from permissions.widgets import role_permission_link


def role_list(request):
    check_permissions(request.user, [PERMISSION_ROLE_VIEW])

    return object_list(
        request,
        queryset=Role.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title': _(u'roles'),
            'hide_link': True,
        },
    )


def role_permissions(request, role_id):
    check_permissions(request.user, [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE])

    role = get_object_or_404(Role, pk=role_id)
    form = RoleForm_view(instance=role)

    role_permissions_list = Permission.objects.get_for_holder(role)
    subtemplates_list = [
        {
            'name': u'generic_list_subtemplate.html',
            'context': {
                'title': _(u'permissions'),
                'object_list': Permission.objects.all(),
                'extra_columns': [
                    {'name': _(u'namespace'), 'attribute': encapsulate(lambda x: namespace_titles[x.namespace] if x.namespace in namespace_titles else x.namespace)},
                    {'name': _(u'name'), 'attribute': u'label'},
                    {
                        'name':_(u'has permission'),
                        'attribute': encapsulate(lambda x: two_state_template(x.has_permission(role))),
                    },
                ],
                'hide_link': True,
                'hide_object': True,
            }
        },
    ]

    return render_to_response('generic_detail.html', {
        'form': form,
        'object': role,
        'object_name': _(u'role'),
        'subtemplates_list': subtemplates_list,
        'multi_select_as_buttons': True,
        'multi_select_item_properties': {
            'permission_id': lambda x: x.pk,
            'requester_id': lambda x: role.pk,
            'requester_app_label': lambda x: ContentType.objects.get_for_model(role).app_label,
            'requester_model': lambda x: ContentType.objects.get_for_model(role).model,
        },
    }, context_instance=RequestContext(request))


def role_edit(request, role_id):
    check_permissions(request.user, [PERMISSION_ROLE_EDIT])

    return update_object(request, template_name='generic_form.html',
        form_class=RoleForm, object_id=role_id, extra_context={
        'object_name': _(u'role')})


def role_create(request):
    check_permissions(request.user, [PERMISSION_ROLE_CREATE])

    return create_object(request, model=Role,
        template_name='generic_form.html',
        post_save_redirect=reverse('role_list'))


def role_delete(request, role_id):
    check_permissions(request.user, [PERMISSION_ROLE_DELETE])

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    return delete_object(request, model=Role, object_id=role_id,
        template_name='generic_confirm.html',
        post_delete_redirect=reverse('role_list'),
        extra_context={
            'delete_view': True,
            'next': next,
            'previous': previous,
            'object_name': _(u'role'),
            'form_icon': u'medal_gold_delete.png',
        })


def permission_grant(request):
    check_permissions(request.user, [PERMISSION_PERMISSION_GRANT])
    items_property_list = loads(request.GET.get('items_property_list', []))
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = []
    for item_properties in items_property_list:
        permission = get_object_or_404(Permission, pk=item_properties['permission_id'])
        ct = get_object_or_404(ContentType, app_label=item_properties['requester_app_label'], model=item_properties['requester_model'])
        requester_model = ct.model_class()
        requester = get_object_or_404(requester_model, pk=item_properties['requester_id'])
        items.append({'requester': requester, 'permission': permission})
        
    sorted_items = sorted(items, key=operator.itemgetter('requester'))
    # Group items by requester
    groups = itertools.groupby(sorted_items, key=operator.itemgetter('requester'))
    grouped_items = [(grouper, [permission['permission'] for permission in group_data]) for grouper, group_data in groups]
    
    # Warning: trial and error black magic ahead
    title_suffix = _(u' and ').join([_(u'%s to %s') % (', '.join(['"%s"' % unicode(ps) for ps in p]), unicode(r)) for r, p in grouped_items])
    
    if len(grouped_items) == 1 and len(grouped_items[0][1]) == 1:
        permissions_label = _(u'permission')
    else:
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
        

def permission_revoke(request):
    check_permissions(request.user, [PERMISSION_PERMISSION_REVOKE])
    items_property_list = loads(request.GET.get('items_property_list', []))
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = []
    for item_properties in items_property_list:
        permission = get_object_or_404(Permission, pk=item_properties['permission_id'])
        ct = get_object_or_404(ContentType, app_label=item_properties['requester_app_label'], model=item_properties['requester_model'])
        requester_model = ct.model_class()
        requester = get_object_or_404(requester_model, pk=item_properties['requester_id'])
        items.append({'requester': requester, 'permission': permission})
        
    sorted_items = sorted(items, key=operator.itemgetter('requester'))
    # Group items by requester
    groups = itertools.groupby(sorted_items, key=operator.itemgetter('requester'))
    grouped_items = [(grouper, [permission['permission'] for permission in group_data]) for grouper, group_data in groups]
    
    # Warning: trial and error black magic ahead
    title_suffix = _(u' and ').join([_(u'%s from %s') % (', '.join(['"%s"' % unicode(ps) for ps in p]), unicode(r)) for r, p in grouped_items])
    
    if len(grouped_items) == 1 and len(grouped_items[0][1]) == 1:
        permissions_label = _(u'permission')
    else:
        permissions_label = _(u'permissions')

    if request.method == 'POST':
        for item in items:
            if item['permission'].revoke_from(item['requester']):
                messages.success(request, _(u'Permission "%(permission)s" revoked from: %(requester)s.') % {
                    'permission': item['permission'], 'requester': item['requester']})
            else:
                messages.warning(request, _(u'%(requester)s, doesn\'t have the permission "%(permission)s" granted.') % {
                    'requester': item['requester'], 'permission': item['permission']})

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'key_delete.png',
    }

    context['title'] = _(u'Are you sure you wish to revoke the %(permissions_label)s %(title_suffix)s?') % {
        'permissions_label': permissions_label,
        'title_suffix': title_suffix,
    }
    
    if len(grouped_items) == 1:
        context['object'] = grouped_items[0][0]

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def get_role_members(role):
    user_ct = ContentType.objects.get(model='user')
    group_ct = ContentType.objects.get(model='group')
    return [member.member_object for member in role.rolemember_set.filter(member_type__in=[user_ct, group_ct])]


def get_non_role_members(role):
    #non members = all users - members - staff - super users
    staff_users = User.objects.filter(is_staff=True)
    super_users = User.objects.filter(is_superuser=True)
    users = set(User.objects.exclude(pk__in=[member.pk for member in get_role_members(role)])) - set(staff_users) - set(super_users)
    groups = set(Group.objects.exclude(pk__in=[member.pk for member in get_role_members(role)]))
    return list(users | groups)


def add_role_member(role, selection):
    model, pk = selection.split(u',')
    ct = ContentType.objects.get(model=model)
    new_member, created = RoleMember.objects.get_or_create(role=role, member_type=ct, member_id=pk)
    if not created:
        raise Exception


def remove_role_member(role, selection):
    model, pk = selection.split(u',')
    ct = ContentType.objects.get(model=model)
    member = RoleMember.objects.get(role=role, member_type=ct, member_id=pk)
    member.delete()


def role_members(request, role_id):
    check_permissions(request.user, [PERMISSION_ROLE_EDIT])
    role = get_object_or_404(Role, pk=role_id)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(get_non_role_members(role)),
        right_list=lambda: generate_choices_w_labels(get_role_members(role)),
        add_method=lambda x: add_role_member(role, x),
        remove_method=lambda x: remove_role_member(role, x),
        left_list_title=_(u'non members of role: %s') % role,
        right_list_title=_(u'members of role: %s') % role,
        extra_context={
            'object': role,
            'object_name': _(u'role'),
        }
    )
