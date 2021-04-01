from django.db.models import Q

from ..models import WebLink

from .literals import (
    TEST_WEB_LINK_LABEL, TEST_WEB_LINK_LABEL_EDITED, TEST_WEB_LINK_TEMPLATE
)


class DocumentTypeAddRemoveWebLinkViewTestMixin:
    def _request_test_document_type_web_link_add_remove_get_view(self):
        return self.get(
            viewname='web_links:document_type_web_links', kwargs={
                'document_type_id': self.test_document_type.pk,
            }
        )

    def _request_test_document_type_web_link_add_view(self):
        return self.post(
            viewname='web_links:document_type_web_links', kwargs={
                'document_type_id': self.test_document_type.pk,
            }, data={
                'available-submit': 'true',
                'available-selection': self.test_web_link.pk
            }
        )

    def _request_test_document_type_web_link_remove_view(self):
        return self.post(
            viewname='web_links:document_type_web_links', kwargs={
                'document_type_id': self.test_document_type.pk,
            }, data={
                'added-submit': 'true',
                'added-selection': self.test_web_link.pk
            }
        )


class ResolvedWebLinkAPIViewTestMixin:
    def _request_resolved_web_link_detail_api_view(self):
        return self.get(
            viewname='rest_api:resolved_web_link-detail',
            kwargs={
                'document_id': self.test_document.pk,
                'resolved_web_link_id': self.test_web_link.pk
            }
        )
        self._create_test_web_link(add_test_document_type=True)

    def _request_resolved_web_link_list_api_view(self):
        return self.get(
            viewname='rest_api:resolved_web_link-list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_resolved_web_link_navigate_api_view(self):
        return self.get(
            viewname='rest_api:resolved_web_link-navigate',
            kwargs={
                'document_id': self.test_document.pk,
                'resolved_web_link_id': self.test_web_link.pk
            }
        )


class WebLinkAPIViewTestMixin:
    def _request_test_web_link_create_api_view(self):
        pk_list = list(WebLink.objects.values('pk'))

        response = self.post(
            viewname='rest_api:web_link-list', data={
                'label': TEST_WEB_LINK_LABEL,
                'template': TEST_WEB_LINK_TEMPLATE
            }
        )

        try:
            self.test_web_link = WebLink.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WebLink.DoesNotExist:
            self.test_web_link = None

        return response

    def _request_test_web_link_delete_api_view(self):
        return self.delete(
            viewname='rest_api:web_link-detail', kwargs={
                'web_link_id': self.test_web_link.pk
            }
        )

    def _request_test_web_link_detail_api_view(self):
        return self.get(
            viewname='rest_api:web_link-detail', kwargs={
                'web_link_id': self.test_web_link.pk
            }
        )

    def _request_test_web_link_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:web_link-detail',
            kwargs={'web_link_id': self.test_web_link.pk}, data={
                'label': TEST_WEB_LINK_LABEL_EDITED,
            }
        )

    def _request_test_web_link_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:web_link-detail',
            kwargs={'web_link_id': self.test_web_link.pk}, data={
                'label': TEST_WEB_LINK_LABEL_EDITED,
                'template': TEST_WEB_LINK_TEMPLATE
            }
        )


class WebLinkDocumentTypeAPIViewMixin:
    def _request_test_web_link_document_type_add_api_view(self):
        return self.post(
            viewname='rest_api:web_link-document_type-add',
            kwargs={'web_link_id': self.test_web_link.pk}, data={
                'document_type': self.test_document_type.pk
            }
        )

    def _request_test_web_link_document_type_list_api_view(self):
        return self.get(
            viewname='rest_api:web_link-document_type-list', kwargs={
                'web_link_id': self.test_web_link.pk,
            }
        )

    def _request_test_web_link_document_type_remove_api_view(self):
        return self.post(
            viewname='rest_api:web_link-document_type-remove',
            kwargs={'web_link_id': self.test_web_link.pk}, data={
                'document_type': self.test_document_type.pk
            }
        )


class WebLinkTestMixin:
    def _create_test_web_link(self, add_test_document_type=False):
        self.test_web_link = WebLink.objects.create(
            label=TEST_WEB_LINK_LABEL, template=TEST_WEB_LINK_TEMPLATE,
        )
        if add_test_document_type:
            self.test_web_link.document_types.add(self.test_document_type)


class WebLinkDocumentTypeViewTestMixin:
    def _request_test_web_link_document_type_add_remove_get_view(self):
        return self.get(
            viewname='web_links:web_link_document_types', kwargs={
                'web_link_id': self.test_web_link.pk
            }
        )

    def _request_test_web_link_document_type_add_view(self):
        return self.post(
            viewname='web_links:web_link_document_types', kwargs={
                'web_link_id': self.test_web_link.pk,
            }, data={
                'available-submit': 'true',
                'available-selection': self.test_document_type.pk
            }
        )

    def _request_test_web_link_document_type_remove_view(self):
        return self.post(
            viewname='web_links:web_link_document_types', kwargs={
                'web_link_id': self.test_web_link.pk,
            }, data={
                'added-submit': 'true',
                'added-selection': self.test_document_type.pk
            }
        )


class WebLinkViewTestMixin:
    def _request_test_document_web_link_instance_view(self):
        return self.post(
            viewname='web_links:web_link_instance_view', kwargs={
                'document_id': self.test_document.pk,
                'web_link_id': self.test_web_link.pk
            }
        )

    def _request_test_document_web_link_list_view(self):
        return self.get(
            viewname='web_links:document_web_link_list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_web_link_create_view(self):
        pk_list = list(WebLink.objects.values('pk'))

        response = self.post(
            viewname='web_links:web_link_create', data={
                'label': TEST_WEB_LINK_LABEL,
                'template_template': TEST_WEB_LINK_TEMPLATE,
            }
        )

        try:
            self.test_web_link = WebLink.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WebLink.DoesNotExist:
            self.test_web_link = None

        return response

    def _request_test_web_link_delete_view(self):
        return self.post(
            viewname='web_links:web_link_delete', kwargs={
                'web_link_id': self.test_web_link.pk
            }
        )

    def _request_test_web_link_edit_view(self):
        return self.post(
            viewname='web_links:web_link_edit', kwargs={
                'web_link_id': self.test_web_link.pk
            }, data={
                'label': TEST_WEB_LINK_LABEL_EDITED,
                'template_template': TEST_WEB_LINK_TEMPLATE
            }
        )

    def _request_test_web_link_list_view(self):
        return self.get(viewname='web_links:web_link_list')
