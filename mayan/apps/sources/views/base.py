import logging

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.navigation.classes import Link
from mayan.apps.views.generics import MultiFormView

from ..icons import icon_upload_view_link
from ..links import factory_conditional_active_by_source
from ..menus import menu_sources
from ..models import Source

logger = logging.getLogger(name=__name__)


class UploadBaseView(MultiFormView):
    object_permission = None
    prefixes = {'source_form': 'source', 'document_form': 'document'}
    template_name = 'appearance/generic_form.html'

    @staticmethod
    def get_tab_link_for_source(source, document=None):
        if document:
            args = ('"{}"'.format(document.pk), '"{}"'.format(source.pk),)
            view = 'sources:document_file_upload'
        else:
            args = ('"{}"'.format(source.pk),)
            view = 'sources:document_upload_interactive'

        return Link(
            args=args,
            conditional_active=factory_conditional_active_by_source(
                source=source
            ), icon=icon_upload_view_link, keep_query=True,
            remove_from_query=['page'], text=source.label, view=view
        )

    def dispatch(self, request, *args, **kwargs):
        self.interactive_sources_enabled = Source.objects.interactive().filter(
            enabled=True
        )

        if not self.interactive_sources_enabled.exists():
            messages.error(
                message=_(
                    'No interactive document sources have been defined or '
                    'none have been enabled, create one before proceeding.'
                ), request=request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(viewname='sources:source_list')
            )

        self.source = self.get_source()

        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as exception:
            if settings.DEBUG:
                raise
            elif request.is_ajax():
                return JsonResponse(
                    data={'error': force_text(s=exception)}, status=500
                )
            else:
                raise

    def get_active_tab_links(self):
        return ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        backend_instance = self.source.get_backend_instance()
        context['source'] = self.source

        context.update(
            backend_instance.get_view_context(
                context=context, request=self.request
            )
        )

        active_link = self.get_active_tab_links()
        menu_sources.bound_links[
            'sources:document_upload_interactive'
        ] = active_link
        menu_sources.bound_links[
            'sources:document_file_upload'
        ] = active_link

        return context

    def get_form_classes(self):
        result = {
            'document_form': self.document_form,
        }

        source_form = self.source.get_backend().get_upload_form_class()
        if source_form:
            result['source_form'] = source_form

        return result

    def get_source(self):
        queryset = self.interactive_sources_enabled

        if self.object_permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=self.object_permission, queryset=queryset,
                user=self.request.user
            )

        if 'source_id' in self.kwargs:
            pk = self.kwargs['source_id']
        else:
            first_source = queryset.first()
            if first_source:
                pk = queryset.first().pk
            else:
                pk = None

        return get_object_or_404(klass=queryset, pk=pk)
