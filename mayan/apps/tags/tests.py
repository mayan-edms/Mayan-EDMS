from django.test import TestCase

from taggit.models import Tag

from .literals import COLOR_RED
from .models import TagProperties


class TagTestCase(TestCase):
    def setUp(self):
        self.tag = Tag(name='test')
        self.tag.save()
        self.tp = TagProperties(tag=self.tag, color=COLOR_RED)
        self.tp.save()

    def runTest(self):
        self.failUnlessEqual(self.tag.name, 'test')
        self.failUnlessEqual(self.tp.get_color_code(), 'red')
