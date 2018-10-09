from __future__ import absolute_import, unicode_literals

TEST_CACHE_KEY_BAD_CHARACTERS = ' \r\n!@#$%^&*()+_{}|:"<>?-=[];\',./'
TEST_DOCUMENT_PK = 99
TEST_NODE_EXPRESSION = 'level_1'
TEST_NODE_EXPRESSION_MULTILINE = 'first\r\nsecond\r\nthird'
TEST_NODE_EXPRESSION_MULTILINE_EXPECTED = 'first second third'
TEST_NODE_EXPRESSION_MULTILINE_2 = '\r\n\r\nfirst\r\nsecond\r\nthird\r\n'
TEST_NODE_EXPRESSION_MULTILINE_2_EXPECTED = 'first second third'
TEST_NODE_PK = 88
TEST_PATH = '/test/path'
