from django.db import models
from django.test import override_settings
from django.utils.encoding import force_text

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.tags.permissions import permission_tag_view
from mayan.apps.tags.search import tag_search
from mayan.apps.tags.tests.mixins import TagTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import SearchModel

from .mixins import SearchTestMixin


class SearchTestCase(SearchTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()

        self.TestModelAttribute = self._create_test_model(
            fields={
                'label': models.CharField(
                    max_length=32
                )
            }, model_name='TestModelAttribute'
        )
        self.TestModelGrandParent = self._create_test_model(
            fields={
                'label': models.CharField(
                    max_length=32
                )
            }, model_name='TestModelGrandParent'
        )
        self.TestModelParent = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelGrandParent',
                ),
                'label': models.CharField(
                    max_length=32
                )
            }, model_name='TestModelParent'
        )

        self.TestModelGrandChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                ),
                'attributes': models.ManyToManyField(
                    related_name='children', to='TestModelAttribute',
                ),
                'label': models.CharField(
                    max_length=32
                )
            }, model_name='TestModelGrandChild'
        )

        # Search setup.

        self._test_search_grandparent = SearchModel(
            app_label=self.TestModelGrandParent._meta.app_label,
            model_name='TestModelGrandParent',
        )

        self._test_search_grandparent.add_model_field(
            field='label'
        )
        self._test_search_grandparent.add_model_field(
            field='children__label'
        )
        self._test_search_grandparent.add_model_field(
            field='children__children__label'
        )
        self._test_search_grandparent.add_model_field(
            field='children__children__attributes__label'
        )

        self._test_search_grandchild = SearchModel(
            app_label=self.TestModelGrandChild._meta.app_label,
            model_name='TestModelGrandChild',
        )
        self._test_search_grandchild.add_model_field(
            field='label'
        )
        self._test_search_grandchild.add_model_field(
            field='attributes__label'
        )

        self._test_search_attribute = SearchModel(
            app_label=self.TestModelAttribute._meta.app_label,
            model_name='TestModelAttribute',
        )
        self._test_search_grandchild.add_model_field(
            field='label'
        )
        self._test_search_attribute.add_model_field(
            field='children__label'
        )

        SearchModel.initialize()

        # Model instances.

        self._test_object_grandparent = self.TestModelGrandParent.objects.create(
            label='grandparent'
        )
        self._test_object_parent = self.TestModelParent.objects.create(
            parent=self._test_object_grandparent,
            label='parent'
        )
        self._test_object_grandchild = self.TestModelGrandChild.objects.create(
            parent=self._test_object_parent,
            label='grandchild'
        )
        self._test_object_attribute = self.TestModelAttribute.objects.create(
            label='attribute'
        )
        self._test_object_grandchild.attributes.add(self._test_object_attribute)

    # Direct object.

    def test_object_field_search(self):
        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'label': self._test_object_grandparent.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

    def test_object_field_update_search(self):
        old_label = self._test_object_grandparent.label
        self._test_object_grandparent.label += 'edited'
        self._test_object_grandparent.save()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'label': self._test_object_grandparent.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'label': '"{}"'.format(old_label)
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    def test_object_field_delete_search(self):
        self._test_object_grandparent.delete()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'label': self._test_object_grandparent.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    # Direct object many to many.

    def test_object_many_to_many_search(self):
        queryset = self.search_backend.search(
            search_model=self._test_search_grandchild,
            query={
                'attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandchild in queryset)

    def test_object_many_to_many_delete_search(self):
        self._test_object_attribute.delete()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandchild,
            query={
                'attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandchild not in queryset)

    def test_object_many_to_many_updated_search(self):
        old_label_value = self._test_object_attribute.label
        self._test_object_attribute.label += 'edited'
        self._test_object_attribute.save()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandchild,
            query={
                'attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandchild in queryset)

        queryset = self.search_backend.search(
            search_model=self._test_search_grandchild,
            query={
                'attributes__label': old_label_value
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandchild not in queryset)

    def test_object_many_to_many_remove_search(self):
        self._test_object_grandchild.attributes.remove(self._test_object_attribute)

        queryset = self.search_backend.search(
            search_model=self._test_search_grandchild,
            query={
                'attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandchild not in queryset)

    def test_object_reverse_many_to_many_search(self):
        queryset = self.search_backend.search(
            search_model=self._test_search_attribute,
            query={
                'children__label': self._test_object_grandchild.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_attribute in queryset)

    # Related object

    def test_object_related_search(self):
        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__label': self._test_object_parent.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

    def test_object_related_delete_search(self):
        self._test_object_parent.delete()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__label': self._test_object_parent.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    def test_object_related_update_search(self):
        old_label_value = self._test_object_parent.label
        self._test_object_parent.label += 'edited'
        self._test_object_parent.save()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__label': self._test_object_parent.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__label': old_label_value
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    def test_object_related_multiple_level_search(self):
        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__label': self._test_object_grandchild.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

    def test_object_related_multiple_level_delete_search(self):
        self._test_object_grandchild.delete()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__label': self._test_object_grandchild.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    def test_object_related_multiple_level_update_search(self):
        old_label_value = self._test_object_grandchild.label
        self._test_object_grandchild.label += 'edited'
        self._test_object_grandchild.save()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__label': self._test_object_grandchild.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__label': old_label_value
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    # Related with many to many

    def test_object_related_multiple_level_many_to_many_search(self):
        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

    def test_object_related_multiple_level_many_to_many_delete_search(self):
        self._test_object_attribute.delete()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    def test_object_related_multiple_level_many_to_many_updated_search(self):
        old_label_value = self._test_object_attribute.label
        self._test_object_attribute.label += 'edited'
        self._test_object_attribute.save()

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent in queryset)

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__attributes__label': old_label_value
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)

    def test_object_related_multiple_level_many_to_many_remove_search(self):
        self._test_object_grandchild.attributes.remove(self._test_object_attribute)

        queryset = self.search_backend.search(
            search_model=self._test_search_grandparent,
            query={
                'children__children__attributes__label': self._test_object_attribute.label
            }, user=self._test_case_user
        )

        self.assertTrue(self._test_object_grandparent not in queryset)


class CommonBackendFunctionalityTestCaseMixin(SearchTestMixin, TagTestMixin):
    def test_advanced_search_related(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={
                'files__mimetype': self.test_document.file_latest.mimetype
            }, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_many_to_many_field(self):
        self._create_test_document_stub()

        self._create_test_tag()

        self.test_tag.documents.add(self.test_document)

        self._index_instance(instance=self.test_document)

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        queryset = self.search_backend.search(
            search_model=tag_search, query={
                'documents__label': self.test_document.label
            }, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_tag in queryset)

    def test_reverse_many_to_many_field_with_multiple_values(self):
        self._create_test_document_stub()

        self._create_test_tag()
        self._create_test_tag()

        self.test_tags[0].documents.add(self.test_document)
        self.test_tags[1].documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        query = {
            'tags__label': self.test_tags[0].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        query = {
            'tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_reverse_many_to_many_field_after_remove_values(self):
        self._create_test_document_stub()

        self._create_test_tag()
        self._create_test_tag()

        self.test_tags[0].documents.add(self.test_document)
        self.test_tags[1].documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        query = {
            'tags__label': self.test_tags[0].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        query = {
            'tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        self.test_tags[1].documents.remove(self.test_document)

        query = {
            'tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)
        self.assertTrue(self.test_document not in queryset)

    def test_related_model_deleted(self):
        self._create_test_document_stub()

        self._create_test_tag()

        self.test_tags[0].documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        query = {
            'tags__label': self.test_tags[0].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        self.test_tag.delete()
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)
        self.assertTrue(self.test_document not in queryset)

    def test_related_model_edited(self):
        self._create_test_document_stub()

        self._create_test_tag()

        self.test_tags[0].documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        old_related_model_field_value = self.test_tags[0].label

        query = {
            'tags__label': self.test_tags[0].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        self.test_tag.label = 'new value'
        self.test_tag.save()

        query = {
            'tags__label': old_related_model_field_value
        }

        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)
        self.assertTrue(self.test_document not in queryset)

        query = {
            'tags__label': self.test_tags[0].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_search_field_transformation_functions(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'uuid': force_text(s=self.test_document.uuid)},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

    def test_undefined_search_field(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        queryset = self.search_backend.search(
            search_model=document_search,
            query={'invalid': 'invalid'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)


@override_settings(SEARCH_BACKEND='mayan.apps.dynamic_search.backends.django.DjangoSearchBackend')
class DjangoSearchBackendDocumentSearchTestCase(
    CommonBackendFunctionalityTestCaseMixin, DocumentTestMixin,
    BaseTestCase
):
    auto_upload_test_document = False

    def test_meta_only(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'OR first'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)

    def test_simple_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'first OR second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_advanced_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )

        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': 'first OR second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_simple_and_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'second non_valid'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_simple_negated_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': '-non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second -Mayan'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second OR -Mayan'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-non_valid -second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_with_dashed_content(self):
        self._upload_test_document(label='second-document')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second-document'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-"second-document"'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)


@override_settings(SEARCH_BACKEND='mayan.apps.dynamic_search.backends.whoosh.WhooshSearchBackend')
class WhooshSearchBackendDocumentSearchTestCase(
    CommonBackendFunctionalityTestCaseMixin, DocumentTestMixin,
    BaseTestCase
):
    auto_upload_test_document = False

    def test_simple_search(self):
        self._upload_test_document(label='first_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'first*'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_meta_only(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'OR first*'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)

    def test_simple_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'first* OR second*'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_advanced_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )

        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': 'first* OR second*'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_simple_and_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'non_valid AND second*'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'second* AND non_valid'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)
