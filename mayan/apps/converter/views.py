from __future__ import absolute_import, unicode_literals

import logging

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
from permissions.models import Permission

from .forms import TransformationForm
from .models import Transformation
from .permissions import (
    PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW
)

logger = logging.getLogger(__name__)


def transformation_list(request, app_label, model, object_id):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model)

    try:
        content_object = content_type.get_object_for_this_type(pk=object_id)
    except content_type.model_class().DoesNotExist:
        raise Http404

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_VIEW, request.user, content_object)

    context = {
        'object_list': Transformation.objects.get_for_model(content_object),
        'content_object': content_object,
        'navigation_object_list': ['content_object'],
        'title': _('Transformations for: %s') % content_object,
        'extra_columns': [
            {'name': _('Order'), 'attribute': 'order'},
            {'name': _('Transformation'), 'attribute': encapsulate(lambda x: x.get_name_display())},
            {'name': _('Arguments'), 'attribute': 'arguments'}
        ],
        'hide_link': True,
        'hide_object': True,
    }
    return render_to_response(
        'appearance/generic_list.html', context, context_instance=RequestContext(request)
    )


def transformation_create(request, app_label, model, object_id):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model)

    try:
        content_object = content_type.get_object_for_this_type(pk=object_id)
    except content_type.model_class().DoesNotExist:
        raise Http404

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_CREATE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_CREATE, request.user, content_object)

    if request.method == 'POST':
        form = TransformationForm(request.POST, initial={'content_object': content_object})
        if form.is_valid():
            instance = form.save(commit=False)
            instance.content_object = content_object
            instance.save()
            messages.success(request, _('Transformation created successfully.'))
            return HttpResponseRedirect(reverse('converter:transformation_list', args=[app_label, model, object_id]))
    else:
        form = TransformationForm(initial={'content_object': content_object})

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'content_object': content_object,
        'navigation_object_list': ['content_object'],
        'title': _('Create new transformation for: %s') % content_object,
    }, context_instance=RequestContext(request))


def transformation_delete(request, object_id):
    transformation = get_object_or_404(Transformation, pk=object_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_DELETE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_DELETE, request.user, transformation.content_object)

    if request.method == 'POST':
        transformation.delete()
        messages.success(request, _('Transformation deleted successfully.'))
        return HttpResponseRedirect(reverse('converter:transformation_list', args=[transformation.content_type.app_label, transformation.content_type.model, transformation.object_id]))

    return render_to_response('appearance/generic_confirm.html', {
        'content_object': transformation.content_object,
        'delete_view': True,
        'navigation_object_list': ['content_object', 'transformation'],
        'previous': reverse('converter:transformation_list', args=[transformation.content_type.app_label, transformation.content_type.model, transformation.object_id]),
        'title': _('Are you sure you wish to delete transformation "%(transformation)s" for: %(content_object)s') % {
            'transformation': transformation,
            'content_object': transformation.content_object},
        'transformation': transformation,
    }, context_instance=RequestContext(request))


def transformation_edit(request, object_id):
    transformation = get_object_or_404(Transformation, pk=object_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_EDIT, request.user, transformation.content_object)

    if request.method == 'POST':
        form = TransformationForm(request.POST, instance=transformation)
        if form.is_valid():
            form.save()
            messages.success(request, _('Transformation edited successfully.'))
            return HttpResponseRedirect(reverse('converter:transformation_list', args=[transformation.content_type.app_label, transformation.content_type.model, transformation.object_id]))
    else:
        form = TransformationForm(instance=transformation)

    return render_to_response('appearance/generic_form.html', {
        'content_object': transformation.content_object,
        'form': form,
        'navigation_object_list': ['content_object', 'transformation'],
        'title': _('Edit transformation "%(transformation)s" for: %(content_object)s') % {
            'transformation': transformation,
            'content_object': transformation.content_object},
        'transformation': transformation,
    }, context_instance=RequestContext(request))
