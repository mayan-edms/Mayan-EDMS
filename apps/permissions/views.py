from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group

from common.forms import ChoiceForm
from common.utils import generate_choices_w_labels

from permissions.models import Role, Permission, PermissionHolder, RoleMember
from permissions.forms import RoleForm, RoleForm_view
from permissions import PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT, \
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, PERMISSION_PERMISSION_GRANT, \
    PERMISSION_PERMISSION_REVOKE
from permissions.api import check_permissions


def role_list(request):
    check_permissions(request.user, 'permissions', [PERMISSION_ROLE_VIEW])

    return object_list(
        request,
        queryset=Role.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title': _(u'roles'),
            'hide_link': True,
        },
    )


def _role_permission_link(requester, permission, permission_list):
    ct = ContentType.objects.get_for_model(requester)

    template = '<span class="nowrap"><a href="%(url)s"><span class="famfam active famfam-%(icon)s"></span>%(text)s</a></span>'

    if permission in permission_list:
        return template % {
            'url': reverse('permission_revoke',
                args=[permission.id, ct.app_label, ct.model, requester.id]),
            'icon': 'delete', 'text': _(u'Revoke')}
    else:
        return template % {
            'url': reverse('permission_grant',
                args=[permission.id, ct.app_label, ct.model, requester.id]),
            'icon': 'add', 'text': _(u'Grant')}


def role_permissions(request, role_id):
    check_permissions(request.user, 'permissions', [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE])

    role = get_object_or_404(Role, pk=role_id)
    form = RoleForm_view(instance=role)

    role_permissions_list = Permission.objects.get_for_holder(role)
    subtemplates_list = [
        {
            'name':'generic_list_subtemplate.html',
            'context': {
                'title':_(u'permissions'),
                'object_list':Permission.objects.all(),
                'extra_columns':[
                    {'name':_(u'namespace'), 'attribute':'namespace'},
                    {'name':_(u'name'), 'attribute':'label'},
                    {
                        'name':_(u'state'),
                        'attribute':lambda x: _role_permission_link(role, x, role_permissions_list),
                    }
                ],
                'hide_link':True,
                'hide_object':True,
            }
        },
    ]

    return render_to_response('generic_detail.html', {
        'form': form,
        'object': role,
        'object_name': _(u'role'),
        'subtemplates_list': subtemplates_list,
    }, context_instance=RequestContext(request))


def role_edit(request, role_id):
    check_permissions(request.user, 'permissions', [PERMISSION_ROLE_EDIT])

    return update_object(request, template_name='generic_form.html',
        form_class=RoleForm, object_id=role_id, extra_context={
        'object_name': _(u'role')})


def role_create(request):
    check_permissions(request.user, 'permissions', [PERMISSION_ROLE_CREATE])

    return create_object(request, model=Role,
        template_name='generic_form.html',
        post_save_redirect=reverse('role_list'))


def role_delete(request, role_id):
    check_permissions(request.user, 'permissions', [PERMISSION_ROLE_DELETE])

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
        })


def permission_grant_revoke(request, permission_id, app_label, module_name, pk, action):
    ct = get_object_or_404(ContentType, app_label=app_label, model=module_name)
    requester_model = ct.model_class()
    requester = get_object_or_404(requester_model, pk=pk)
    permission = get_object_or_404(Permission, pk=permission_id)

    if action == 'grant':
        check_permissions(request.user, 'permissions', [PERMISSION_PERMISSION_GRANT])
        title = _(u'Are you sure you wish to grant the permission "%(permission)s" to %(ct_name)s: %(requester)s') % {
            'permission': permission, 'ct_name': ct.name, 'requester': requester}

    elif action == 'revoke':
        check_permissions(request.user, 'permissions', [PERMISSION_PERMISSION_REVOKE])
        title = _(u'Are you sure you wish to revoke the permission "%(permission)s" from %(ct_name)s: %(requester)s') % {
            'permission': permission, 'ct_name': ct.name, 'requester': requester}
    else:
        return HttpResponseRedirect(u'/')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        if action == 'grant':
            permission_holder, created = PermissionHolder.objects.get_or_create(permission=permission, holder_type=ct, holder_id=requester.id)
            if created:
                messages.success(request, _(u'Permission "%(permission)s" granted to %(ct_name)s: %(requester)s.') % {
                    'permission': permission, 'ct_name': ct.name, 'requester': requester})
            else:
                messages.warning(request, _(u'%(ct_name)s: %(requester)s, already had the permission "%(permission)s" granted.') % {
                    'ct_name': ct.name, 'requester': requester, 'permission': permission})
        elif action == 'revoke':
            try:
                permission_holder = PermissionHolder.objects.get(permission=permission, holder_type=ct, holder_id=requester.id)
                permission_holder.delete()
                messages.success(request, _(u'Permission "%(permission)s" revoked from %(ct_name)s: %(requester)s.') % {
                    'permission': permission, 'ct_name': ct.name, 'requester': requester})
            except ObjectDoesNotExist:
                messages.warning(request, _(u'%(ct_name)s: %(requester)s doesn\'t have the permission "%(permission)s".') % {
                    'ct_name': ct.name, 'requester': requester, 'permission': permission})
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': requester,
        'next': next,
        'previous': previous,
        'title': title,
    }, context_instance=RequestContext(request))


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


def role_members(request, role_id):
    check_permissions(request.user, 'permissions', [PERMISSION_ROLE_EDIT])
    role = get_object_or_404(Role, pk=role_id)

    if request.method == 'POST':
        if 'unselected-users-submit' in request.POST.keys():
            unselected_users_form = ChoiceForm(request.POST,
                prefix='unselected-users',
                choices=generate_choices_w_labels(get_non_role_members(role)))
            if unselected_users_form.is_valid():
                for selection in unselected_users_form.cleaned_data['selection']:
                    model, pk = selection.split(u',')
                    ct = ContentType.objects.get(model=model)
                    obj = ct.get_object_for_this_type(pk=pk)
                    new_member, created = RoleMember.objects.get_or_create(role=role, member_type=ct, member_id=pk)
                    if created:
                        messages.success(request, _(u'%(obj)s added successfully to the role: %(role)s.') % {
                            'obj': generate_choices_w_labels([obj])[0][1], 'role': role})

        elif 'selected-users-submit' in request.POST.keys():
            selected_users_form = ChoiceForm(request.POST,
                prefix='selected-users',
                choices=generate_choices_w_labels(get_role_members(role)))
            if selected_users_form.is_valid():
                for selection in selected_users_form.cleaned_data['selection']:
                    model, pk = selection.split(u',')
                    ct = ContentType.objects.get(model=model)
                    obj = ct.get_object_for_this_type(pk=pk)

                    try:
                        member = RoleMember.objects.get(role=role, member_type=ct, member_id=pk)
                        member.delete()
                        messages.success(request, _(u'%(obj)s removed successfully from the role: %(role)s.') % {
                            'obj': generate_choices_w_labels([obj])[0][1], 'role': role})
                    except member.DoesNotExist:
                        messages.error(request, _(u'Unable to remove %(obj)s from the role: %(role)s.') % {
                            'obj': generate_choices_w_labels([obj])[0][1], 'role': role})

    unselected_users_form = ChoiceForm(prefix='unselected-users',
        choices=generate_choices_w_labels(get_non_role_members(role)))
    selected_users_form = ChoiceForm(prefix='selected-users',
        choices=generate_choices_w_labels(get_role_members(role)))

    context = {
        'object': role,
        'object_name': _(u'role'),
        'form_list': [
            {
                'form': unselected_users_form,
                'title': _(u'non members of role: %s') % role,
                'grid': 6,
                'grid_clear': False,
                'submit_label': _(u'Add'),
            },
            {
                'form': selected_users_form,
                'title': _(u'members of role: %s') % role,
                'grid': 6,
                'grid_clear': True,
                'submit_label': _(u'Remove'),
            },

        ],
    }

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))
