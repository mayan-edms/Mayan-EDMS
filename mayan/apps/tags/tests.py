from django.test import TestCase

from .literals import COLOR_RED
from .models import Tag


class TagTestCase(TestCase):
    def setUp(self):
        self.tag = Tag(label='test', color=COLOR_RED)
        self.tag.save()

    def runTest(self):
        self.failUnlessEqual(self.tag.label, 'test')
        self.failUnlessEqual(self.tag.get_color_code(), 'red')

# TODO: Add test for attaching and removing documents to a tag
