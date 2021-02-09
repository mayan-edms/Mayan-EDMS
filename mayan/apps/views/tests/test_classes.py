from mayan.apps.testing.tests.base import BaseTestCase

from ..http import URL


class URLTestCase(BaseTestCase):
    def test_query_to_string(self):
        url = URL(query={'a': 1})

        self.assertEqual(url.to_string(), '?a=1')

    def test_query_list_to_string(self):
        url = URL(query={'a': '1'})
        url.args.appendlist(key='a', value='2')

        self.assertEqual(url.to_string(), '?a=1&a=2')

    def test_query_with_question_mark_to_string(self):
        url = URL(query={'a': '1?'})

        self.assertEqual(url.to_string(), '?a=1%3F')

    def test_querystring_with_list_to_string(self):
        url = URL(query_string='a=1&a=2')

        self.assertEqual(url.args.getlist('a'), ['1', '2'])

    def test_querystring_with_question_mark_to_string(self):
        url = URL(query_string='a=1?')

        self.assertEqual(url.to_string(), '?a=1%3F')

    def test_querystring_with_question_mark_encoded_to_string(self):
        url = URL(query_string='a=1%3F')

        self.assertEqual(url.to_string(), '?a=1%3F')

    def test_querystring_to_args(self):
        url = URL(query_string='a=1')

        self.assertEqual(url.args['a'], '1')

    def test_querystring_with_question_mark_encoded_to_args(self):
        url = URL(query_string='a=1%3F')

        self.assertEqual(url.args['a'], '1?')

    def test_querystring_mixed_to_args(self):
        url = URL(query_string='a=1&a=2&b=1')

        self.assertEqual(url.args.getlist('a'), ['1', '2'])
        self.assertEqual(url.args.getlist('b'), ['1'])

    def test_path_and_querystring_to_string(self):
        url = URL(path='http://example.com', query_string='a=1')

        self.assertEqual(url.to_string(), 'http://example.com?a=1')

    def test_path_and_query_to_string(self):
        url = URL(path='http://example.com', query={'a': 1})

        self.assertEqual(url.to_string(), 'http://example.com?a=1')
