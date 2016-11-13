from __future__ import absolute_import, unicode_literals

import logging
import urlparse

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from acls.models import AccessControlList
from common.generics import SimpleView, SingleObjectListView
from converter.literals import DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL

from ..forms import DocumentPageForm
from ..models import Document, DocumentPage
from ..permissions import permission_document_view
from ..settings import (
    setting_rotation_step, setting_zoom_percent_step, setting_zoom_max_level,
    setting_zoom_min_level
)

logger = logging.getLogger(__name__)


class DocumentPageListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=self.request.user,
            obj=self.get_document()
        )

        return super(
            DocumentPageListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_document().pages.all()

    def get_extra_context(self):
        return {
            'object': self.get_document(),
            'title': _('Pages for document: %s') % self.get_document(),
        }


class DocumentPageView(SimpleView):
    template_name = 'appearance/generic_form.html'

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=request.user,
            obj=self.get_object().document
        )

        return super(
            DocumentPageView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        zoom = int(self.request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))
        rotation = int(self.request.GET.get('rotation', DEFAULT_ROTATION))

        document_page_form = DocumentPageForm(
            instance=self.get_object(), zoom=zoom, rotation=rotation
        )

        base_title = _('Image of: %s') % self.get_object()

        if zoom != DEFAULT_ZOOM_LEVEL:
            zoom_text = '({}%)'.format(zoom)
        else:
            zoom_text = ''

        return {
            'form': document_page_form,
            'hide_labels': True,
            'navigation_object_list': ('page',),
            'page': self.get_object(),
            'rotation': rotation,
            'title': ' '.join((base_title, zoom_text,)),
            'read_only': True,
            'zoom': zoom,
        }

    def get_object(self):
        return get_object_or_404(DocumentPage, pk=self.kwargs['pk'])


class DocumentPageViewResetView(RedirectView):
    pattern_name = 'documents:document_page_view'


def document_page_navigation_next(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    AccessControlList.objects.check_access(
        permissions=permission_document_view, user=request.user,
        obj=document_page.document
    )

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    if document_page.page_number >= document_page.siblings.count():
        messages.warning(request, _('There are no more pages in this document'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    else:
        document_page = get_object_or_404(document_page.siblings, page_number=document_page.page_number + 1)
        return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


def document_page_navigation_previous(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    AccessControlList.objects.check_access(
        permissions=permission_document_view, user=request.user,
        obj=document_page.document
    )

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    if document_page.page_number <= 1:
        messages.warning(request, _('You are already at the first page of this document'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    else:
        document_page = get_object_or_404(document_page.siblings, page_number=document_page.page_number - 1)
        return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


def document_page_navigation_first(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(document_page.siblings, page_number=1)

    AccessControlList.objects.check_access(
        permissions=permission_document_view, user=request.user,
        obj=document_page.document
    )

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


def document_page_navigation_last(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(document_page.siblings, page_number=document_page.siblings.count())

    AccessControlList.objects.check_access(
        permissions=permission_document_view, user=request.user,
        obj=document_page.document
    )

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


class DocumentPageInteractiveTransformation(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()

        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=request.user,
            obj=object
        )

        return super(DocumentPageInteractiveTransformation, self).dispatch(
            request, *args, **kwargs
        )

    def get_object(self):
        return get_object_or_404(DocumentPage, pk=self.kwargs['pk'])

    def get_redirect_url(self, *args, **kwargs):
        url = reverse(
            'documents:document_page_view', args=(self.kwargs['pk'],)
        )

        query_dict = {
            'rotation': int(self.request.GET.get('rotation', DEFAULT_ROTATION)),
            'zoom': int(self.request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))
        }

        self.transformation_function(query_dict)

        return '{}?{}'.format(url, urlencode(query_dict))


class DocumentPageZoomInView(DocumentPageInteractiveTransformation):
    def transformation_function(self, query_dict):
        zoom = query_dict['zoom'] + setting_zoom_percent_step.value

        if zoom > setting_zoom_max_level.value:
            zoom = setting_zoom_max_level.value

        query_dict['zoom'] = zoom


class DocumentPageZoomOutView(DocumentPageInteractiveTransformation):
    def transformation_function(self, query_dict):
        zoom = query_dict['zoom'] - setting_zoom_percent_step.value

        if zoom < setting_zoom_min_level.value:
            zoom = setting_zoom_min_level.value

        query_dict['zoom'] = zoom


class DocumentPageRotateLeftView(DocumentPageInteractiveTransformation):
    def transformation_function(self, query_dict):
        query_dict['rotation'] = (
            query_dict['rotation'] - setting_rotation_step.value
        ) % 360


class DocumentPageRotateRightView(DocumentPageInteractiveTransformation):
    def transformation_function(self, query_dict):
        query_dict['rotation'] = (
            query_dict['rotation'] + setting_rotation_step.value
        ) % 360
