from ..models import WebLink

from .literals import (
    TEST_WEB_LINK_LABEL, TEST_WEB_LINK_LABEL_EDITED, TEST_WEB_LINK_TEMPLATE
)


class ResolvedWebLinkAPIViewTestMixin(object):
    def _request_resolved_web_link_detail_view(self):
        return self.get(
            viewname='rest_api:resolved_web_link-detail',
            kwargs={
                'pk': self.test_document.pk,
                'resolved_web_link_pk': self.test_web_link.pk
            }
        )
        self._create_test_web_link(add_test_document_type=True)

    def _request_resolved_web_link_list_view(self):
        return self.get(
            viewname='rest_api:resolved_web_link-list', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_resolved_web_link_navigate_view(self):
        return self.get(
            viewname='rest_api:resolved_web_link-navigate',
            kwargs={
                'pk': self.test_document.pk,
                'resolved_web_link_pk': self.test_web_link.pk
            }
        )


class WebLinkAPIViewTestMixin(object):
    def _request_test_web_link_create_api_view(self):
        return self.post(
            viewname='rest_api:web_link-list', data={
                'label': TEST_WEB_LINK_LABEL,
                'template': TEST_WEB_LINK_TEMPLATE
            }
        )

    def _request_test_web_link_create_with_document_type_api_view(self):
        return self.post(
            viewname='rest_api:web_link-list', data={
                'label': TEST_WEB_LINK_LABEL,
                'document_types_pk_list': self.test_document_type.pk,
                'template': TEST_WEB_LINK_TEMPLATE
            },
        )

    def _request_test_web_link_delete_api_view(self):
        return self.delete(
            viewname='rest_api:web_link-detail', kwargs={
                'pk': self.test_web_link.pk
            }
        )

    def _request_test_web_link_detail_api_view(self):
        return self.get(
            viewname='rest_api:web_link-detail', kwargs={
                'pk': self.test_web_link.pk
            }
        )

    def _request_test_web_link_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:web_link-detail',
            kwargs={'pk': self.test_web_link.pk}, data={
                'label': TEST_WEB_LINK_LABEL_EDITED,
                'document_types_pk_list': self.test_document_type.pk
            }
        )

    def _request_test_web_link_edit_put_api_view(self):
        return self.put(
            viewname='rest_api:web_link-detail',
            kwargs={'pk': self.test_web_link.pk}, data={
                'label': TEST_WEB_LINK_LABEL_EDITED,
                'document_types_pk_list': self.test_document_type.pk,
                'template': TEST_WEB_LINK_TEMPLATE
            }
        )


class WebLinkTestMixin(object):
    def _create_test_web_link(self, add_document_type=False):
        self.test_web_link = WebLink.objects.create(
            label=TEST_WEB_LINK_LABEL, template=TEST_WEB_LINK_TEMPLATE,
        )
        if add_document_type:
            self.test_web_link.document_types.add(self.test_document_type)


class WebLinkViewTestMixin(object):
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
        return self.post(
            viewname='web_links:web_link_create', data={
                'label': TEST_WEB_LINK_LABEL,
                'template_template': TEST_WEB_LINK_TEMPLATE,
            }
        )

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
