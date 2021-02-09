from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import TemplateTagTestMixin


class TemplateFilterDictGetTestCase(TemplateTagTestMixin, BaseTestCase):
    def test_filter_dict_get_valid(self):
        result = self._render_test_template(
            template_string='{{ dict|dict_get:1 }}', context={'dict': {1: 'a'}}
        )
        self.assertEqual(result, 'a')

    def test_filter_dict_get_invalid(self):
        result = self._render_test_template(
            template_string='{{ dict|dict_get:2 }}', context={'dict': {1: 'a'}}
        )
        self.assertEqual(result, '')


class TemplateFilterSplitTestCase(TemplateTagTestMixin, BaseTestCase):
    def test_filter_split_valid(self):
        result = self._render_test_template(
            template_string='{% with x|split:"," as result %}{{ result.0 }}-{{ result.1 }}-{{ result.2 }}{% endwith %}', context={'x': '1,2,3'}
        )
        self.assertEqual(result, '1-2-3')


class TemplateTagRegexTestCase(TemplateTagTestMixin, BaseTestCase):
    def test_tag_regex_findall_false(self):
        result = self._render_test_template(
            template_string='{% regex_findall "\\d" "abcxyz" as result %}{% if result %}{{ result }}{% endif %}'
        )
        self.assertEqual(result, '')

    def test_tag_regex_findall_true(self):
        result = self._render_test_template(
            template_string='{% regex_findall "\\d" "abc123" as result %}{{ result.0 }}{{ result.1 }}{{ result.2 }}'
        )
        self.assertEqual(result, '123')

    def test_tag_regex_match_false(self):
        result = self._render_test_template(
            template_string='{% regex_match "\\d" "abc123" as result %}{% if result %}{{ result }}{% endif %}'
        )
        self.assertEqual(result, '')

    def test_tag_regex_match_true(self):
        result = self._render_test_template(
            template_string='{% regex_match "\\d" "123abc" as result %}{% if result %}{{ result.0 }}{% endif %}'
        )
        self.assertEqual(result, '1')

    def test_tag_regex_search_false(self):
        result = self._render_test_template(
            template_string='{% regex_search "\\d" "abcxyz" as result %}{% if result %}{{ result }}{% endif %}'
        )
        self.assertEqual(result, '')

    def test_tag_regex_search_true(self):
        result = self._render_test_template(
            template_string='{% regex_search "\\d" "abc123" as result %}{{ result.0 }}'
        )
        self.assertEqual(result, '1')

    def test_tag_regex_sub_false(self):
        result = self._render_test_template(
            template_string='{% regex_sub "\\d" "XX" "abcxyz" as result %}{{ result }}'
        )
        self.assertEqual(result, 'abcxyz')

    def test_tag_regex_sub_true(self):
        result = self._render_test_template(
            template_string='{% regex_sub "\\d" "XX" "abc123" as result %}{{ result }}'
        )
        self.assertEqual(result, 'abcXXXXXX')


class TemplateTagSetTestCase(TemplateTagTestMixin, BaseTestCase):
    def test_tag_set_string(self):
        result = self._render_test_template(
            template_string='{% set "string" as result %}{{ result }}'
        )
        self.assertEqual(result, 'string')

    def test_tag_set_number(self):
        result = self._render_test_template(
            template_string='{% set 99 as result %}{{ result }}'
        )
        self.assertEqual(result, '99')

    def test_tag_set_logical(self):
        result = self._render_test_template(
            template_string='{% set True as result %}{{ result }}'
        )
        self.assertEqual(result, 'True')

    def test_tag_set_nonexistant(self):
        result = self._render_test_template(
            template_string='{% set nonexistant as result %}{{ result }}'
        )
        self.assertEqual(result, '')
