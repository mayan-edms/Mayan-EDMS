import logging

from furl import furl

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _, ungettext
from django.views.generic import RedirectView

from mayan.apps.common.classes import ModelQueryFields
from mayan.apps.common.settings import setting_home_view
from mayan.apps.converter.literals import DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL
from mayan.apps.views.generics import (
    FormView, MultipleObjectConfirmActionView, SingleObjectDeleteView,
    SingleObjectListView, SimpleView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin
from mayan.apps.views.utils import resolve

from ..forms.document_version_page_forms import (
    DocumentVersionPageForm, DocumentVersionPageMappingFormSet
)
from ..icons import (
    icon_document_version_page_list, icon_document_version_page_list_remap
)
from ..links.document_version_page_links import (
    link_document_version_page_list_remap,
    link_document_version_page_list_reset
)
from ..models.document_version_models import DocumentVersion
from ..models.document_version_page_models import DocumentVersionPage
from ..permissions import (
    permission_document_version_edit, permission_document_version_view
)
from ..settings import (
    setting_rotation_step, setting_zoom_percent_step, setting_zoom_max_level,
    setting_zoom_min_level
)
from ..tasks import task_document_version_page_list_reset

__all__ = (
    'DocumentVersionPageListView',
    'DocumentVersionPageNavigationFirst', 'DocumentVersionPageNavigationLast',
    'DocumentVersionPageNavigationNext', 'DocumentVersionPageNavigationPrevious',
    'DocumentVersionPageView', 'DocumentVersionPageViewResetView',
    'DocumentVersionPageInteractiveTransformation', 'DocumentVersionPageZoomInView',
    'DocumentVersionPageZoomOutView', 'DocumentVersionPageRotateLeftView',
    'DocumentVersionPageRotateRightView'
)
logger = logging.getLogger(name=__name__)


class DocumentVersionPageDeleteView(SingleObjectDeleteView):
    object_permission = permission_document_version_edit
    pk_url_kwarg = 'document_version_page_id'
    source_queryset = DocumentVersionPage.valid

    def get_extra_context(self):
        return {
            'message': _(
                'The page number of this page will be skipped. If you '
                'want to achieve sequential page numbering, use the '
                'page remap action instead.'
            ),
            'object': self.object,
            'title': _('Delete document version page %s ?') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_version_page_list', kwargs={
                'document_version_id': self.object.document_version_id
            }
        )


class DocumentVersionPageListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_permission = permission_document_version_view
    external_object_pk_url_kwarg = 'document_version_id'
    external_object_queryset = DocumentVersion.valid

    def get_extra_context(self):
        return {
            'hide_object': True,
            'list_as_items': True,
            'no_results_icon': icon_document_version_page_list,
            'no_results_main_link': link_document_version_page_list_reset.resolve(
                request=self.request, resolved_object=self.external_object
            ),
            'no_results_secondary_links': [
                link_document_version_page_list_remap.resolve(
                    request=self.request, resolved_object=self.external_object
                ),
            ],
            'no_results_text': _(
                'Document version pages are links to actual content pages. '
                'Create them using the page remap actions or the page '
                'reset action.'
            ),
            'no_results_title': _('No document version pages available'),
            'object': self.external_object,
            'title': _('Pages of document version: %s') % self.external_object,
        }

    def get_source_queryset(self):
        queryset = ModelQueryFields.get(model=DocumentVersionPage).get_queryset()
        return queryset.filter(pk__in=self.external_object.pages.all())


class DocumentVersionPageListRemapView(ExternalObjectViewMixin, FormView):
    external_object_permission = permission_document_version_edit
    external_object_pk_url_kwarg = 'document_version_id'
    external_object_queryset = DocumentVersion.valid
    form_class = DocumentVersionPageMappingFormSet

    def form_valid(self, form):
        annotated_content_object_list = []

        for row in form.forms:
            page_number = int(row.cleaned_data['target_page_number'])
            if page_number:
                content_type = ContentType.objects.get(
                    pk=row.cleaned_data['source_content_type']
                )
                content_object = content_type.get_object_for_this_type(
                    pk=row.cleaned_data['source_object_id']
                )

                annotated_content_object_list.append(
                    {
                        'page_number': page_number,
                        'content_object': content_object
                    }
                )

        self.external_object.pages_remap(
            annotated_content_object_list=annotated_content_object_list
        )
        return super().form_valid(form=form)

    def get_form_extra_kwargs(self):
        target_page_number_choices = [(0, _('None'))]

        page_index = 1

        for document_file in self.external_object.document.files.all():
            for document_file_page in document_file.pages.all():
                target_page_number_choices.append(
                    (page_index, page_index)
                )

                page_index = page_index + 1

        return {
            'form_extra_kwargs': {
                'target_page_number_choices': target_page_number_choices
            }
        }

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'hide_object': True,
            'list_as_items': True,
            'no_results_icon': icon_document_version_page_list_remap,
            'no_results_text': _(
                'There are no sources available to remap for this document '
                'version.'
            ),
            'no_results_title': _('No page sources available'),
            'object': self.external_object,
            'title': _(
                'Remap pages of document version: %s'
            ) % self.external_object,
        }

    def get_initial(self):
        initial = []

        content_object_dictionary_list = self.external_object.get_source_content_object_dictionary_list()

        for content_object_dictionary in content_object_dictionary_list:
            content_object = content_object_dictionary['content_type'].get_object_for_this_type(
                id=content_object_dictionary['object_id']
            )

            # The same source object could have been assigned to multiple
            # document version pages.
            document_version_pages = self.external_object.pages.filter(
                content_type=content_object_dictionary['content_type'],
                object_id=content_object_dictionary['object_id']
            )

            if document_version_pages:
                document_version_page_page_number = document_version_pages.first().page_number
            else:
                document_version_page_page_number = 0

            row = {
                'source_content_type': content_object_dictionary['content_type'].pk,
                'source_object_id': content_object_dictionary['object_id'],
                'source_thumbnail': content_object,
                'source_label': '{}: {}'.format(content_object_dictionary['content_type'].name, content_object),
                'target_page_number': document_version_page_page_number
            }

            initial.append(row)

        return initial

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_version_page_list', kwargs={
                'document_version_id': self.external_object.pk
            }
        )


class DocumentVersionPageListResetView(MultipleObjectConfirmActionView):
    object_permission = permission_document_version_edit
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid
    success_message = _(
        '%(count)d document version queued for page list reset.'
    )
    success_message_plural = _(
        '%(count)d document versions queued for page list reset.'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'message': _(
                'The page list will match that of the latest document file.'
            ),
            'title': ungettext(
                singular='Reset the page list of the selected document version?',
                plural='Reset the page list of the selected document versions?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Reset the page list of document version: %s?'
                    ) % queryset.first()
                }
            )

        return result

    def object_action(self, form, instance):
        task_document_version_page_list_reset.apply_async(
            kwargs={'document_version_id': instance.pk}
        )


class DocumentVersionPageNavigationBase(ExternalObjectViewMixin, RedirectView):
    external_object_permission = permission_document_version_view
    external_object_pk_url_kwarg = 'document_version_page_id'
    external_object_queryset = DocumentVersionPage.valid

    def get_redirect_url(self, *args, **kwargs):
        """
        Attempt to jump to the same kind of view but resolved to a new
        object of the same kind.
        """
        previous_url = self.request.META.get('HTTP_REFERER', None)

        if not previous_url:
            try:
                previous_url = self.external_object.get_absolute_url()
            except AttributeError:
                previous_url = reverse(viewname=setting_home_view.value)

        parsed_url = furl(url=previous_url)

        # Obtain the view name to be able to resolve it back with new keyword
        # arguments.
        resolver_match = resolve(path=force_text(s=parsed_url.path))

        new_kwargs = self.get_new_kwargs()

        if set(new_kwargs) == set(resolver_match.kwargs):
            # It is the same type of object, reuse the URL to stay in the
            # same kind of view but pointing to a new object
            url = reverse(
                viewname=resolver_match.view_name, kwargs=new_kwargs
            )
        else:
            url = parsed_url.path

        # Update just the path to retain the querystring in case there is
        # transformation data.
        parsed_url.path = url

        return parsed_url.tostr()


class DocumentVersionPageNavigationFirst(DocumentVersionPageNavigationBase):
    def get_new_kwargs(self):
        return {
            'document_version_page_id': self.external_object.siblings.first().pk
        }


class DocumentVersionPageNavigationLast(DocumentVersionPageNavigationBase):
    def get_new_kwargs(self):
        return {
            'document_version_page_id': self.external_object.siblings.last().pk
        }


class DocumentVersionPageNavigationNext(DocumentVersionPageNavigationBase):
    def get_new_kwargs(self):
        new_document_version_page = self.external_object.siblings.filter(
            page_number__gt=self.external_object.page_number
        ).first()
        if new_document_version_page:
            return {'document_version_page_id': new_document_version_page.pk}
        else:
            messages.warning(
                message=_(
                    'There are no more pages in this document'
                ), request=self.request
            )
            return {'document_version_page_id': self.external_object.pk}


class DocumentVersionPageNavigationPrevious(DocumentVersionPageNavigationBase):
    def get_new_kwargs(self):
        new_document_version_page = self.external_object.siblings.filter(
            page_number__lt=self.external_object.page_number
        ).last()
        if new_document_version_page:
            return {'document_version_page_id': new_document_version_page.pk}
        else:
            messages.warning(
                message=_(
                    'You are already at the first page of this document'
                ), request=self.request
            )
            return {'document_version_page_id': self.external_object.pk}


class DocumentVersionPageView(ExternalObjectViewMixin, SimpleView):
    external_object_permission = permission_document_version_view
    external_object_pk_url_kwarg = 'document_version_page_id'
    external_object_queryset = DocumentVersionPage.valid
    template_name = 'appearance/generic_form.html'

    def get_extra_context(self):
        zoom = int(self.request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))
        rotation = int(self.request.GET.get('rotation', DEFAULT_ROTATION))

        document_version_page_form = DocumentVersionPageForm(
            instance=self.external_object, rotation=rotation, zoom=zoom
        )

        base_title = _('Image of: %s') % self.external_object

        if zoom != DEFAULT_ZOOM_LEVEL:
            zoom_text = '({}%)'.format(zoom)
        else:
            zoom_text = ''

        return {
            'form': document_version_page_form,
            'hide_labels': True,
            'object': self.external_object,
            'rotation': rotation,
            'title': ' '.join((base_title, zoom_text)),
            'read_only': True,
            'zoom': zoom,
        }


class DocumentVersionPageViewResetView(RedirectView):
    pattern_name = 'documents:document_version_page_view'


class DocumentVersionPageInteractiveTransformation(
    ExternalObjectViewMixin, RedirectView
):
    external_object_permission = permission_document_version_view
    external_object_pk_url_kwarg = 'document_version_page_id'
    external_object_queryset = DocumentVersionPage.valid

    def get_object(self):
        return self.external_object

    def get_redirect_url(self, *args, **kwargs):
        query_dict = {
            'rotation': self.request.GET.get('rotation', DEFAULT_ROTATION),
            'zoom': self.request.GET.get('zoom', DEFAULT_ZOOM_LEVEL)
        }

        url = furl(
            args=query_dict, path=reverse(
                viewname='documents:document_version_page_view', kwargs={
                    'document_version_page_id': self.external_object.pk
                }
            )

        )

        self.transformation_function(query_dict=query_dict)
        # Refresh query_dict to args reference
        url.args = query_dict

        return url.tostr()


class DocumentVersionPageZoomInView(
    DocumentVersionPageInteractiveTransformation
):
    def transformation_function(self, query_dict):
        zoom = int(query_dict['zoom']) + setting_zoom_percent_step.value

        if zoom > setting_zoom_max_level.value:
            zoom = setting_zoom_max_level.value

        query_dict['zoom'] = zoom


class DocumentVersionPageZoomOutView(
    DocumentVersionPageInteractiveTransformation
):
    def transformation_function(self, query_dict):
        zoom = int(query_dict['zoom']) - setting_zoom_percent_step.value

        if zoom < setting_zoom_min_level.value:
            zoom = setting_zoom_min_level.value

        query_dict['zoom'] = zoom


class DocumentVersionPageRotateLeftView(
    DocumentVersionPageInteractiveTransformation
):
    def transformation_function(self, query_dict):
        query_dict['rotation'] = (
            int(query_dict['rotation']) - setting_rotation_step.value
        ) % 360


class DocumentVersionPageRotateRightView(
    DocumentVersionPageInteractiveTransformation
):
    def transformation_function(self, query_dict):
        query_dict['rotation'] = (
            int(query_dict['rotation']) + setting_rotation_step.value
        ) % 360
