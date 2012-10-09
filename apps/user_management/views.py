from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from permissions.models import Permission
from common.utils import generate_choices_w_labels, encapsulate
from common.widgets import two_state_template
from common.views import assign_remove

from .permissions import (PERMISSION_USER_CREATE, PERMISSION_USER_EDIT,
    PERMISSION_USER_VIEW, PERMISSION_USER_DELETE, PERMISSION_GROUP_CREATE,
    PERMISSION_GROUP_EDIT, PERMISSION_GROUP_VIEW, PERMISSION_GROUP_DELETE)
from .forms import UserForm, PasswordForm, GroupForm


def user_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_USER_VIEW])

    return object_list(
        request,
        queryset=User.objects.exclude(is_superuser=True).exclude(is_staff=True).order_by('username'),
        template_name='generic_list.html',
        extra_context={
            'title': _(u'users'),
            'hide_link': True,
            'extra_columns': [
                {
                    'name': _(u'full name'),
                    'attribute': 'get_full_name'
                },
                {
                    'name': _(u'email'),
                    'attribute': 'email'
                },
                {
                    'name': _(u'active'),
                    'attribute': encapsulate(lambda x: two_state_template(x.is_active)),
                },
                {
                    'name': _(u'has usable password?'),
                    'attribute': encapsulate(lambda x: two_state_template(x.has_usable_password())),
                },
            ],
            'multi_select_as_buttons': True,
        },
    )


def user_edit(request, user_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_USER_EDIT])
    user = get_object_or_404(User, pk=user_id)

    if user.is_superuser or user.is_staff:
        messages.error(request, _(u'Super user and staff user editing is not allowed, use the admin interface for these cases.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        form = UserForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'User "%s" updated successfully.') % user)
            return HttpResponseRedirect(reverse('user_list'))
    else:
        form = UserForm(instance=user)

    return render_to_response('generic_form.html', {
        'title': _(u'edit user: %s') % user,
        'form': form,
        'object': user,
        'object_name': _(u'user'),
    },
    context_instance=RequestContext(request))


def user_add(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_USER_CREATE])

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_unusable_password()
            user.save()
            messages.success(request, _(u'User "%s" created successfully.') % user)
            return HttpResponseRedirect(reverse('user_set_password', args=[user.pk]))
    else:
        form = UserForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create new user'),
        'form': form,
    },
    context_instance=RequestContext(request))


def user_delete(request, user_id=None, user_id_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_USER_DELETE])
    post_action_redirect = None

    if user_id:
        users = [get_object_or_404(User, pk=user_id)]
        post_action_redirect = reverse('user_list')
    elif user_id_list:
        users = [get_object_or_404(User, pk=user_id) for user_id in user_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one user.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for user in users:
            try:
                if user.is_superuser or user.is_staff:
                    messages.error(request, _(u'Super user and staff user deleting is not allowed, use the admin interface for these cases.'))
                else:
                    user.delete()
                    messages.success(request, _(u'User "%s" deleted successfully.') % user)
            except Exception, e:
                messages.error(request, _(u'Error deleting user "%(user)s": %(error)s') % {
                    'user': user, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'user'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'user_delete.png',
    }
    if len(users) == 1:
        context['object'] = users[0]
        context['title'] = _(u'Are you sure you wish to delete the user: %s?') % ', '.join([unicode(d) for d in users])
    elif len(users) > 1:
        context['title'] = _(u'Are you sure you wish to delete the users: %s?') % ', '.join([unicode(d) for d in users])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def user_multiple_delete(request):
    return user_delete(
        request, user_id_list=request.GET.get('id_list', [])
    )


def user_set_password(request, user_id=None, user_id_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_USER_EDIT])
    post_action_redirect = None

    if user_id:
        users = [get_object_or_404(User, pk=user_id)]
        post_action_redirect = reverse('user_list')
    elif user_id_list:
        users = [get_object_or_404(User, pk=user_id) for user_id in user_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one user.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password_1 = form.cleaned_data['new_password_1']
            password_2 = form.cleaned_data['new_password_2']
            if password_1 != password_2:
                messages.error(request, _(u'Passwords do not match, try again.'))
            else:
                for user in users:
                    try:
                        if user.is_superuser or user.is_staff:
                            messages.error(request, _(u'Super user and staff user password reseting is not allowed, use the admin interface for these cases.'))
                        else:
                            user.set_password(password_1)
                            user.save()
                            messages.success(request, _(u'Successfull password reset for user: %s.') % user)
                    except Exception, e:
                        messages.error(request, _(u'Error reseting password for user "%(user)s": %(error)s') % {
                            'user': user, 'error': e
                        })

                return HttpResponseRedirect(next)
    else:
        form = PasswordForm()

    context = {
        'object_name': _(u'user'),
        'next': next,
        'form': form,
    }

    if len(users) == 1:
        context['object'] = users[0]
        context['title'] = _(u'Reseting password for user: %s') % ', '.join([unicode(d) for d in users])
    elif len(users) > 1:
        context['title'] = _(u'Reseting password for users: %s') % ', '.join([unicode(d) for d in users])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def user_multiple_set_password(request):
    return user_set_password(
        request, user_id_list=request.GET.get('id_list', [])
    )


def get_user_groups(user):
    #return user.group_set.all()
    return Group.objects.filter(user=user)


def get_user_non_groups(user):
    return Group.objects.exclude(user=user)


def user_groups(request, user_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_USER_EDIT])
    user = get_object_or_404(User, pk=user_id)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(get_user_non_groups(user), display_object_type=False),
        right_list=lambda: generate_choices_w_labels(get_user_groups(user), display_object_type=False),
        add_method=lambda x: x.user_set.add(user),
        remove_method=lambda x: x.user_set.remove(user),
        left_list_title=_(u'non groups of user: %s') % user,
        right_list_title=_(u'groups of user: %s') % user,
        decode_content_type=True,
        extra_context={
            'object': user,
            'object_name': _(u'user'),
        }
    )


# Group views
def group_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_GROUP_VIEW])

    return object_list(
        request,
        queryset=Group.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title': _(u'groups'),
            'hide_link': True,
            'extra_columns': [
                {
                    'name': _(u'members'),
                    'attribute': 'user_set.count'
                },
            ],
            'multi_select_as_buttons': True,
        },
    )


def group_edit(request, group_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_GROUP_EDIT])
    group = get_object_or_404(Group, pk=group_id)

    if request.method == 'POST':
        form = GroupForm(instance=group, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Group "%s" updated successfully.') % group)
            return HttpResponseRedirect(reverse('group_list'))
    else:
        form = GroupForm(instance=group)

    return render_to_response('generic_form.html', {
        'title': _(u'edit group: %s') % group,
        'form': form,
        'object': group,
        'object_name': _(u'group'),
    },
    context_instance=RequestContext(request))


def group_add(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_GROUP_CREATE])

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, _(u'Group "%s" created successfully.') % group)
            return HttpResponseRedirect(reverse('group_list'))
    else:
        form = GroupForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create new group'),
        'form': form,
    },
    context_instance=RequestContext(request))


def group_delete(request, group_id=None, group_id_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_GROUP_DELETE])
    post_action_redirect = None

    if group_id:
        groups = [get_object_or_404(Group, pk=group_id)]
        post_action_redirect = reverse('group_list')
    elif group_id_list:
        groups = [get_object_or_404(Group, pk=group_id) for group_id in group_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one group.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for group in groups:
            try:
                group.delete()
                messages.success(request, _(u'Group "%s" deleted successfully.') % group)
            except Exception, e:
                messages.error(request, _(u'Error deleting group "%(group)s": %(error)s') % {
                    'group': group, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'group'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'group_delete.png',
    }
    if len(groups) == 1:
        context['object'] = groups[0]
        context['title'] = _(u'Are you sure you wish to delete the group: %s?') % ', '.join([unicode(d) for d in groups])
    elif len(groups) > 1:
        context['title'] = _(u'Are you sure you wish to delete the groups: %s?') % ', '.join([unicode(d) for d in groups])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def group_multiple_delete(request):
    return group_delete(
        request, group_id_list=request.GET.get('id_list', [])
    )


def get_group_members(group):
    return group.user_set.all()


def get_non_group_members(group):
    return User.objects.exclude(groups=group).exclude(is_staff=True).exclude(is_superuser=True)


def group_members(request, group_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_GROUP_EDIT])
    group = get_object_or_404(Group, pk=group_id)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(get_non_group_members(group), display_object_type=False),
        right_list=lambda: generate_choices_w_labels(get_group_members(group), display_object_type=False),
        add_method=lambda x: group.user_set.add(x),
        remove_method=lambda x: group.user_set.remove(x),
        left_list_title=_(u'non members of group: %s') % group,
        right_list_title=_(u'members of group: %s') % group,
        decode_content_type=True,
        extra_context={
            'object': group,
            'object_name': _(u'group'),
        }
    )
