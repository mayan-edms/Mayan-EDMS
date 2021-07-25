from mayan.apps.testing.tests.base import BaseTestCase

from ..http import URL


class URLTestCase(BaseTestCase):
    def test_query_list_to_string(self):
        url = URL(query={'a': [1, 2]})

        self.assertEqual(url.to_string(), '?a=1&a=2')

    def test_query_string_to_string(self):
        url = URL(url='http://example.com?a=1', query={'a': 'string'})

        self.assertEqual(url.to_string(), 'http://example.com?a=string')

    def test_query_to_string(self):
        url = URL(query={'a': 1})

        self.assertEqual(url.to_string(), '?a=1')

    def test_query_list_append_to_string(self):
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
        url = URL(url='http://example.com', query_string='a=1')

        self.assertEqual(url.to_string(), 'http://example.com?a=1')

    def test_path_and_query_to_string(self):
        url = URL(url='http://example.com', query={'a': 1})

        self.assertEqual(url.to_string(), 'http://example.com?a=1')

    def test_port_set(self):
        url = URL(scheme='http', netloc='127.0.0.1', port='9999')

        self.assertEqual(url.to_string(), 'http://127.0.0.1:9999')

    def test_port_replace(self):
        url = URL(port='9999', url='https://127.0.0.1:8888')

        self.assertEqual(url.to_string(), 'https://127.0.0.1:9999')

    def test_scheme_set(self):
        url = URL(scheme='http', netloc='127.0.0.1')

        self.assertEqual(url.to_string(), 'http://127.0.0.1')

    def test_scheme_replace(self):
        url = URL(scheme='http', url='https://127.0.0.1')

        self.assertEqual(url.to_string(), 'http://127.0.0.1')

    def test_path_viewname_exclusion(self):
        with self.assertRaises(expected_exception=RuntimeError):
            URL(path='/view', viewname='app:viewname')

    def test_path_replace(self):
        url = URL(url='http://127.0.0.1:8000/view_a', path='view_b')

        self.assertEqual(url.to_string(), 'http://127.0.0.1:8000/view_b')
