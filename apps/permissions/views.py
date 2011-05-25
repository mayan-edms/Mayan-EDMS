from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
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

from common.views import assign_remove
from common.utils import generate_choices_w_labels

from permissions.models import Role, Permission, PermissionHolder, RoleMember
from permissions.forms import RoleForm, RoleForm_view
from permissions import PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT, \
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, PERMISSION_PERMISSION_GRANT, \
    PERMISSION_PERMISSION_REVOKE
from permissions.api import check_permissions, namespace_titles


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


def _role_permission_link(requester, permission, permission_list):
    ct = ContentType.objects.get_for_model(requester)

    template = u'<span class="nowrap"><a href="%(url)s"><span class="famfam active famfam-%(icon)s"></span>%(text)s</a></span>'

    if permission in permission_list:
        return template % {
            'url': reverse('permission_revoke',
                args=[permission.pk, ct.app_label, ct.model, requester.pk]),
            'icon': u'key_delete', 'text': ugettext(u'Revoke')}
    else:
        return template % {
            'url': reverse('permission_grant',
                args=[permission.pk, ct.app_label, ct.model, requester.pk]),
            'icon': u'key_add', 'text': ugettext(u'Grant')}


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
                    {'name': _(u'namespace'), 'attribute': lambda x: namespace_titles[x.namespace] if x.namespace in namespace_titles else x.namespace},
                    {'name': _(u'name'), 'attribute': u'label'},
                    {
                        'name':_(u'state'),
                        'attribute': lambda x: _role_permission_link(role, x, role_permissions_list),
                    }
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


def permission_grant_revoke(request, permission_id, app_label, module_name, pk, action):
    ct = get_object_or_404(ContentType, app_label=app_label, model=module_name)
    requester_model = ct.model_class()
    requester = get_object_or_404(requester_model, pk=pk)
    permission = get_object_or_404(Permission, pk=permission_id)

    if action == 'grant':
        check_permissions(request.user, [PERMISSION_PERMISSION_GRANT])
        title = _(u'Are you sure you wish to grant the permission "%(permission)s" to %(ct_name)s: %(requester)s') % {
            'permission': permission, 'ct_name': ct.name, 'requester': requester}
        icon_name = u'key_add.png'
    elif action == 'revoke':
        check_permissions(request.user, [PERMISSION_PERMISSION_REVOKE])
        title = _(u'Are you sure you wish to revoke the permission "%(permission)s" from %(ct_name)s: %(requester)s') % {
            'permission': permission, 'ct_name': ct.name, 'requester': requester}
        icon_name = u'key_delete.png'
    else:
        return HttpResponseRedirect(u'/')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        if action == 'grant':
            permission_holder, created = PermissionHolder.objects.get_or_create(permission=permission, holder_type=ct, holder_id=requester.pk)
            if created:
                messages.success(request, _(u'Permission "%(permission)s" granted to %(ct_name)s: %(requester)s.') % {
                    'permission': permission, 'ct_name': ct.name, 'requester': requester})
            else:
                messages.warning(request, _(u'%(ct_name)s: %(requester)s, already had the permission "%(permission)s" granted.') % {
                    'ct_name': ct.name, 'requester': requester, 'permission': permission})
        elif action == 'revoke':
            try:
                permission_holder = PermissionHolder.objects.get(permission=permission, holder_type=ct, holder_id=requester.pk)
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
        'form_icon': icon_name,
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
        obj=role,
        object_name=_(u'role'),
    )
