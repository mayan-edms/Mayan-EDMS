from __future__ import absolute_import, unicode_literals

from common.tests import BaseTestCase

from ..caches import IndexFilesystemCache

from .literals import TEST_DOCUMENT_PK, TEST_NODE_PK, TEST_PATH


class MockDocument(object):
    pk = TEST_DOCUMENT_PK


class MockNode(object):
    pk = TEST_NODE_PK


class IndexFilesystemCacheTestCase(BaseTestCase):
    def setUp(self):
        super(IndexFilesystemCacheTestCase, self).setUp()
        self.cache = IndexFilesystemCache()
        self.document = MockDocument()
        self.node = MockNode()

    def test_set_path_document(self):
        self.cache.set_path(path=TEST_PATH, document=self.document)
        self.assertEquals(
            {'document_pk': TEST_DOCUMENT_PK},
            self.cache.get_path(path=TEST_PATH)
        )

    def test_set_path_document_clear_document(self):
        self.cache.set_path(path=TEST_PATH, document=self.document)
        self.cache.clear_document(document=self.document)

        self.assertEquals(None, self.cache.get_path(path=TEST_PATH))

    def test_set_path_node(self):
        self.cache.set_path(path=TEST_PATH, node=self.node)
        self.assertEquals(
            {'node_pk': TEST_NODE_PK},
            self.cache.get_path(path=TEST_PATH)
        )

    def test_set_path_node_clear_node(self):
        self.cache.set_path(path=TEST_PATH, node=self.node)
        self.cache.clear_node(node=self.node)

        self.assertEquals(None, self.cache.get_path(path=TEST_PATH))
