from __future__ import unicode_literals

import itertools
from json import loads
import operator

from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.classes import EncapsulatedObject
from common.models import AnonymousUserSingleton
from common.views import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    assign_remove
)
from common.utils import encapsulate, get_object_name
from common.widgets import two_state_template

from .forms import RoleForm, RoleForm_view
from .models import Permission, Role
from .permissions import (
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE,
    PERMISSION_ROLE_VIEW, PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE,
    PERMISSION_ROLE_EDIT
)


class RoleCreateView(SingleObjectCreateView):
    form_class = RoleForm
    model = Role
    view_permission = PERMISSION_ROLE_CREATE
    success_url = reverse_lazy('permissions:role_list')


class RoleDeleteView(SingleObjectDeleteView):
    model = Role
    view_permission = PERMISSION_ROLE_DELETE
    success_url = reverse_lazy('permissions:role_list')


class RoleEditView(SingleObjectEditView):
    model = Role
    view_permission = PERMISSION_ROLE_EDIT


def role_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_ROLE_VIEW])

    context = {
        'object_list': Role.objects.all(),
        'title': _('Roles'),
        'hide_link': True,
    }

    return render_to_response('main/generic_list.html', context,
                              context_instance=RequestContext(request))


def role_permissions(request, role_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE])

    role = get_object_or_404(Role, pk=role_id)
    form = RoleForm_view(instance=role)

    subtemplates_list = [
        {
            'name': 'main/generic_list_subtemplate.html',
            'context': {
                'title': _('Permissions'),
                'object_list': Permission.objects.all(),
                'extra_columns': [
                    {'name': _('Namespace'), 'attribute': encapsulate(lambda x: x.namespace)},
                    {'name': _('Name'), 'attribute': encapsulate(lambda x: x.label)},
                    {
                        'name': _('Has permission'),
                        'attribute': encapsulate(lambda x: two_state_template(x.requester_has_this(role))),
                    },
                ],
                'hide_link': True,
                'hide_object': True,
            }
        },
    ]

    return render_to_response('main/generic_detail.html', {
        'form': form,
        'object': role,
        'subtemplates_list': subtemplates_list,
        'multi_select_item_properties': {
            'permission_id': lambda x: x.pk,
            'requester_id': lambda x: role.pk,
            'requester_app_label': lambda x: ContentType.objects.get_for_model(role).app_label,
            'requester_model': lambda x: ContentType.objects.get_for_model(role).model,
        },
    }, context_instance=RequestContext(request))


def permission_grant(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_PERMISSION_GRANT])
    items_property_list = loads(request.GET.get('items_property_list', []))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    items = []
    for item_properties in items_property_list:
        try:
            permission = Permission.objects.get({'pk': item_properties['permission_id']})
        except Permission.DoesNotExist:
            raise Http404

        ct = get_object_or_404(ContentType, app_label=item_properties['requester_app_label'], model=item_properties['requester_model'])
        requester_model = ct.model_class()
        requester = get_object_or_404(requester_model, pk=item_properties['requester_id'])
        items.append({'requester': requester, 'permission': permission})

    sorted_items = sorted(items, key=operator.itemgetter('requester'))
    # Group items by requester
    groups = itertools.groupby(sorted_items, key=operator.itemgetter('requester'))
    grouped_items = [(grouper, [permission['permission'] for permission in group_data]) for grouper, group_data in groups]

    # Warning: trial and error black magic ahead
    title_suffix = _(' and ').join([_('%(permissions)s to %(requester)s') % {'permissions': ', '.join(['"%s"' % unicode(ps) for ps in p]), 'requester': unicode(r)} for r, p in grouped_items])

    if len(grouped_items) == 1 and len(grouped_items[0][1]) == 1:
        permissions_label = _('Permission')
    else:
        permissions_label = _('Permissions')

    if request.method == 'POST':
        for item in items:
            if item['permission'].grant_to(item['requester']):
                messages.success(request, _('Permission "%(permission)s" granted to: %(requester)s.') % {
                    'permission': item['permission'], 'requester': item['requester']})
            else:
                messages.warning(request, _('%(requester)s, already had the permission "%(permission)s" granted.') % {
                    'requester': item['requester'], 'permission': item['permission']})

        return HttpResponseRedirect(next)

    context = {
        'previous': previous,
        'next': next,
    }

    context['title'] = _('Are you sure you wish to grant the %(permissions_label)s %(title_suffix)s?') % {
        'permissions_label': permissions_label,
        'title_suffix': title_suffix,
    }

    if len(grouped_items) == 1:
        context['object'] = grouped_items[0][0]

    return render_to_response('main/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def permission_revoke(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_PERMISSION_REVOKE])
    items_property_list = loads(request.GET.get('items_property_list', []))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    items = []
    for item_properties in items_property_list:
        try:
            permission = Permission.objects.get({'pk': item_properties['permission_id']})
        except Permission.DoesNotExist:
            raise Http404

        ct = get_object_or_404(ContentType, app_label=item_properties['requester_app_label'], model=item_properties['requester_model'])
        requester_model = ct.model_class()
        requester = get_object_or_404(requester_model, pk=item_properties['requester_id'])
        items.append({'requester': requester, 'permission': permission})

    sorted_items = sorted(items, key=operator.itemgetter('requester'))
    # Group items by requester
    groups = itertools.groupby(sorted_items, key=operator.itemgetter('requester'))
    grouped_items = [(grouper, [permission['permission'] for permission in group_data]) for grouper, group_data in groups]

    # Warning: trial and error black magic ahead
    title_suffix = _(' and ').join([_('%(permissions)s to %(requester)s') % {'permissions': ', '.join(['"%s"' % unicode(ps) for ps in p]), 'requester': unicode(r)} for r, p in grouped_items])

    if len(grouped_items) == 1 and len(grouped_items[0][1]) == 1:
        permissions_label = _('permission')
    else:
        permissions_label = _('permissions')

    if request.method == 'POST':
        for item in items:
            if item['permission'].revoke_from(item['requester']):
                messages.success(request, _('Permission "%(permission)s" revoked from: %(requester)s.') % {
                    'permission': item['permission'], 'requester': item['requester']})
            else:
                messages.warning(request, _('%(requester)s, doesn\'t have the permission "%(permission)s" granted.') % {
                    'requester': item['requester'], 'permission': item['permission']})

        return HttpResponseRedirect(next)

    context = {
        'previous': previous,
        'next': next,
    }

    context['title'] = _('Are you sure you wish to revoke the %(permissions_label)s %(title_suffix)s?') % {
        'permissions_label': permissions_label,
        'title_suffix': title_suffix,
    }

    if len(grouped_items) == 1:
        context['object'] = grouped_items[0][0]

    return render_to_response('main/generic_confirm.html', context,
                              context_instance=RequestContext(request))


class Member(EncapsulatedObject):
    source_object_name = 'member_object'


def _as_choice_list(items):
    return sorted([(Member.encapsulate(item).gid, get_object_name(item, display_object_type=False)) for item in items], key=lambda x: x[1])


def get_role_members(role, separate=False):
    user_ct = ContentType.objects.get(model='user')
    group_ct = ContentType.objects.get(model='group')
    anonymous = ContentType.objects.get(model='anonymoususersingleton')

    users = role.members(filter_dict={'member_type': user_ct})
    groups = role.members(filter_dict={'member_type': group_ct})
    anonymous = role.members(filter_dict={'member_type': anonymous})

    if separate:
        return users, groups, anonymous
    else:
        members = []

        if users:
            members.append((_('Users'), _as_choice_list(list(users))))

        if groups:
            members.append((_('Groups'), _as_choice_list(list(groups))))

        if anonymous:
            members.append((_('Special'), _as_choice_list(list(anonymous))))

        return members


def get_non_role_members(role):
    # non members = all users - members - staff - super users
    member_users, member_groups, member_anonymous = get_role_members(role, separate=True)

    staff_users = User.objects.filter(is_staff=True)
    super_users = User.objects.filter(is_superuser=True)

    users = set(User.objects.all()) - set(member_users) - set(staff_users) - set(super_users)
    groups = set(Group.objects.all()) - set(member_groups)
    anonymous = set([AnonymousUserSingleton.objects.get()]) - set(member_anonymous)

    non_members = []
    if users:
        non_members.append((_('Users'), _as_choice_list(list(users))))

    if groups:
        non_members.append((_('Groups'), _as_choice_list(list(groups))))

    if anonymous:
        non_members.append((_('Special'), _as_choice_list(list(anonymous))))

    return non_members


def add_role_member(role, selection):
    member = Member.get(selection).source_object
    role.add_member(member)


def remove_role_member(role, selection):
    member = Member.get(selection).source_object
    role.remove_member(member)


def role_members(request, role_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_ROLE_EDIT])
    role = get_object_or_404(Role, pk=role_id)

    return assign_remove(
        request,
        left_list=lambda: get_non_role_members(role),
        right_list=lambda: get_role_members(role),
        add_method=lambda x: add_role_member(role, x),
        remove_method=lambda x: remove_role_member(role, x),
        left_list_title=_('Non members of role: %s') % role,
        right_list_title=_('Members of role: %s') % role,
        extra_context={
            'object': role,
        },
        grouped=True,
    )
