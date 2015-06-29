from __future__ import absolute_import, unicode_literals

import logging
from json import loads

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from common.widgets import two_state_template
from permissions import Permission

from .api import get_class_permissions_for
from .classes import AccessHolder, AccessObject, AccessObjectClass
from .forms import ClassHolderSelectionForm, HolderSelectionForm
from .models import AccessEntry
from .permissions import acls_edit_acl, acls_view_acl
from .widgets import object_indentifier

logger = logging.getLogger(__name__)


def _permission_titles(permission_list):
    return ', '.join([unicode(permission) for permission in permission_list])


def acl_list_for(request, obj, extra_context=None):
    try:
        Permission.check_permissions(request.user, [acls_view_acl])
    except PermissionDenied:
        AccessEntry.objects.check_access(acls_view_acl, request.user, obj)

    logger.debug('obj: %s', obj)

    context = {
        'object_list': AccessEntry.objects.get_holders_for(obj),
        'title': _('Access control lists for: %s' % obj),
        'extra_columns': [
            {'name': _('Holder'), 'attribute': encapsulate(lambda x: object_indentifier(x.source_object))},
            {'name': _('Permissions'), 'attribute': encapsulate(lambda x: _permission_titles(AccessEntry.objects.get_holder_permissions_for(obj, x.source_object, db_only=True)))},
        ],
        'hide_object': True,
        'access_object': AccessObject.encapsulate(obj),
        'object': obj,
        'navigation_object_list': ['object', 'access_object'],
    }

    if extra_context:
        context.update(extra_context)

    return render_to_response('appearance/generic_list.html', context,
                              context_instance=RequestContext(request))


def acl_list(request, app_label, model_name, object_id):
    ct = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    obj = get_object_or_404(ct.get_object_for_this_type, pk=object_id)
    return acl_list_for(request, obj)


def acl_detail(request, access_object_gid, holder_object_gid):
    try:
        holder = AccessHolder.get(gid=holder_object_gid)
        access_object = AccessObject.get(gid=access_object_gid)
    except ObjectDoesNotExist:
        raise Http404

    # return acl_detail_for(request, holder.source_object, access_object.source_object)
    return acl_detail_for(request, holder, access_object)


def acl_detail_for(request, actor, obj):
    try:
        Permission.check_permissions(request.user, [acls_view_acl])
    except PermissionDenied:
        AccessEntry.objects.check_accesses([acls_view_acl], actor, obj)

    permission_list = get_class_permissions_for(obj.source_object)
    # TODO : get all globally assigned permission, new function get_permissions_for_holder (roles aware)
    subtemplates_list = [
        {
            'name': 'appearance/generic_list_subtemplate.html',
            'context': {
                'title': _('Permissions available to: %(actor)s for %(obj)s' % {
                    'actor': actor,
                    'obj': obj
                }
                ),
                'object_list': permission_list,
                'extra_columns': [
                    {'name': _('Namespace'), 'attribute': 'namespace'},
                    {'name': _('Label'), 'attribute': 'label'},
                    {
                        'name': _('Has permission'),
                        'attribute': encapsulate(lambda permission: two_state_template(AccessEntry.objects.has_access(permission, actor, obj, db_only=True)))
                    },
                ],
                'hide_object': True,
            }
        },
    ]

    context = {
        'object': obj.source_object,
        'subtemplates_list': subtemplates_list,
        'multi_select_item_properties': {
            'permission_pk': lambda x: x.pk,
            'holder_gid': lambda x: actor.gid,
            'object_gid': lambda x: obj.gid,
        },
        'access_object': obj,
        'navigation_object_list': ['object', 'access_object'],
        'read_only': True,
    }

    return render_to_response('appearance/generic_form.html', context,
                              context_instance=RequestContext(request))


def acl_grant(request):
    items_property_list = loads(request.GET.get('items_property_list', []))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    items = {}
    title_suffix = []
    navigation_object = None
    navigation_object_count = 0

    for item_properties in items_property_list:
        try:
            permission = Permission.get({'pk': item_properties['permission_pk']})
        except Permission.DoesNotExist:
            raise Http404

        try:
            requester = AccessHolder.get(gid=item_properties['holder_gid'])
            access_object = AccessObject.get(gid=item_properties['object_gid'])
        except ObjectDoesNotExist:
            raise Http404

        try:
            Permission.check_permissions(request.user, [acls_edit_acl])
        except PermissionDenied:
            try:
                AccessEntry.objects.check_access(acls_edit_acl, request.user, access_object)
            except PermissionDenied:
                raise
            else:
                items.setdefault(requester, {})
                items[requester].setdefault(access_object, [])
                items[requester][access_object].append(permission)
                navigation_object = access_object
                navigation_object_count += 1
        else:
            items.setdefault(requester, {})
            items[requester].setdefault(access_object, [])
            items[requester][access_object].append(permission)
            navigation_object = access_object
            navigation_object_count += 1

    for requester, obj_ps in items.items():
        for obj, ps in obj_ps.items():
            title_suffix.append(_(', ').join(['"%s"' % unicode(p) for p in ps]))
            title_suffix.append(_(' for %s') % obj)
        title_suffix.append(_(' to %s') % requester)

    if len(items_property_list) == 1:
        title_prefix = _('Are you sure you wish to grant the permission %(title_suffix)s?')
    else:
        title_prefix = _('Are you sure you wish to grant the permissions %(title_suffix)s?')

    if request.method == 'POST':
        for requester, object_permissions in items.items():
            for obj, permissions in object_permissions.items():
                for permission in permissions:
                    if AccessEntry.objects.grant(permission, requester.source_object, obj.source_object):
                        messages.success(request, _('Permission "%(permission)s" granted to %(actor)s for %(object)s.') % {
                            'permission': permission,
                            'actor': requester,
                            'object': obj
                        })
                    else:
                        messages.warning(request, _('%(actor)s, already had the permission "%(permission)s" granted for %(object)s.') % {
                            'actor': requester,
                            'permission': permission,
                            'object': obj,
                        })

        return HttpResponseRedirect(next)

    context = {
        'previous': previous,
        'next': next,
    }

    context['title'] = title_prefix % {
        'title_suffix': ''.join(title_suffix),
    }

    logger.debug('navigation_object_count: %d', navigation_object_count)
    logger.debug('navigation_object: %s', navigation_object)
    if navigation_object_count == 1:
        context['object'] = navigation_object.source_object

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def acl_revoke(request):
    items_property_list = loads(request.GET.get('items_property_list', []))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    items = {}
    title_suffix = []
    navigation_object = None
    navigation_object_count = 0

    for item_properties in items_property_list:
        try:
            permission = Permission.get({'pk': item_properties['permission_pk']})
        except Permission.DoesNotExist:
            raise Http404

        try:
            requester = AccessHolder.get(gid=item_properties['holder_gid'])
            access_object = AccessObject.get(gid=item_properties['object_gid'])
        except ObjectDoesNotExist:
            raise Http404

        try:
            Permission.check_permissions(request.user, [acls_edit_acl])
        except PermissionDenied:
            try:
                AccessEntry.objects.check_access(acls_edit_acl, request.user, access_object)
            except PermissionDenied:
                raise
            else:
                items.setdefault(requester, {})
                items[requester].setdefault(access_object, [])
                items[requester][access_object].append(permission)
                navigation_object = access_object
                navigation_object_count += 1
        else:
            items.setdefault(requester, {})
            items[requester].setdefault(access_object, [])
            items[requester][access_object].append(permission)
            navigation_object = access_object
            navigation_object_count += 1

    for requester, obj_ps in items.items():
        for obj, ps in obj_ps.items():
            title_suffix.append(_(', ').join(['"%s"' % unicode(p) for p in ps]))
            title_suffix.append(_(' for %s') % obj)
        title_suffix.append(_(' from %s') % requester)

    if len(items_property_list) == 1:
        title_prefix = _('Are you sure you wish to revoke the permission %(title_suffix)s?')
    else:
        title_prefix = _('Are you sure you wish to revoke the permissions %(title_suffix)s?')

    if request.method == 'POST':
        for requester, object_permissions in items.items():
            for obj, permissions in object_permissions.items():
                for permission in permissions:
                    if AccessEntry.objects.revoke(permission, requester.source_object, obj.source_object):
                        messages.success(request, _('Permission "%(permission)s" revoked of %(actor)s for %(object)s.') % {
                            'permission': permission,
                            'actor': requester,
                            'object': obj
                        })
                    else:
                        messages.warning(request, _('%(actor)s, didn\'t had the permission "%(permission)s" for %(object)s.') % {
                            'actor': requester,
                            'permission': permission,
                            'object': obj,
                        })

        return HttpResponseRedirect(next)

    context = {
        'previous': previous,
        'next': next,
    }

    context['title'] = title_prefix % {
        'title_suffix': ''.join(title_suffix),
    }

    logger.debug('navigation_object_count: %d', navigation_object_count)
    logger.debug('navigation_object: %s', navigation_object)
    if navigation_object_count == 1:
        context['object'] = navigation_object.source_object

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def acl_new_holder_for(request, obj, extra_context=None, navigation_object=None):
    try:
        Permission.check_permissions(request.user, [acls_edit_acl])
    except PermissionDenied:
        AccessEntry.objects.check_access(acls_edit_acl, request.user, obj)

    if request.method == 'POST':
        form = HolderSelectionForm(request.POST)
        if form.is_valid():
            try:
                access_object = AccessObject.encapsulate(obj)
                access_holder = AccessHolder.get(form.cleaned_data['holder_gid'])

                query_string = {'navigation_object': navigation_object}

                return HttpResponseRedirect(
                    '%s?%s' % (
                        reverse('acls:acl_detail', args=[access_object.gid, access_holder.gid]),
                        urlencode(query_string)
                    )
                )
            except ObjectDoesNotExist:
                raise Http404
    else:
        form = HolderSelectionForm()

    context = {
        'form': form,
        'title': _('Add new holder for: %s') % obj,
        'submit_label': _('Select'),
        'object': obj,
        'access_object': AccessObject.encapsulate(obj),
        'navigation_object_list': ['object', 'access_object'],
    }

    if extra_context:
        context.update(extra_context)

    return render_to_response('appearance/generic_form.html', context,
                              context_instance=RequestContext(request))


def acl_holder_new(request, access_object_gid):
    try:
        access_object = AccessObject.get(gid=access_object_gid)
    except ObjectDoesNotExist:
        raise Http404

    return acl_new_holder_for(request, access_object.source_object)
