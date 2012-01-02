from django.utils import unittest

from .models import Tag, TagProperties
from .literals import COLOR_RED


class TagTestCase(unittest.TestCase):
    def setUp(self):
        self.tag = Tag(name='test')
        self.tag.save()
        self.tp = TagProperties(tag=self.tag, color=COLOR_RED)
        self.tp.save()

    def runTest(self):
        self.failUnlessEqual(self.tag.name, 'test')
        self.failUnlessEqual(self.tp.get_color_code(), 'red')
