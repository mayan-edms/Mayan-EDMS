from __future__ import unicode_literals

from ..models import MetadataType

from .literals import (
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_LABEL_EDITED,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_NAME_EDITED
)


class MetadataTypeTestMixin(object):
    def setUp(self):
        super(MetadataTypeTestMixin, self).setUp()
        self.metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )


class MetadataTestsMixin(object):
    def _create_metadata_type(self):
        self.metadata_type = MetadataType.objects.create(
            label=TEST_METADATA_TYPE_LABEL,
            name=TEST_METADATA_TYPE_NAME
        )

    def _request_metadata_type_create_view(self):
        return self.post(
            viewname='metadata:setup_metadata_type_create', data={
                'label': TEST_METADATA_TYPE_LABEL,
                'name': TEST_METADATA_TYPE_NAME
            }
        )

    def _request_metadata_type_delete_view(self):
        return self.post(
            viewname='metadata:setup_metadata_type_delete', args=(
                self.metadata_type.pk,
            ),
        )

    def _request_metadata_type_edit_view(self):
        return self.post(
            viewname='metadata:setup_metadata_type_edit', args=(
                self.metadata_type.pk,), data={
                'label': TEST_METADATA_TYPE_LABEL_EDITED,
                'name': TEST_METADATA_TYPE_NAME_EDITED
            }
        )

    def _request_metadata_type_relationship_edit_view(self):
        # This request assumes there is only one document type and
        # blindly sets the first form of the formset.

        return self.post(
            viewname='metadata:setup_metadata_type_document_types',
            args=(self.metadata_type.pk,), data={
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-0-relationship_type': 'required',
            }
        )

    def _request_metadata_type_list_view(self):
        return self.get(
            viewname='metadata:setup_metadata_type_list',
        )
