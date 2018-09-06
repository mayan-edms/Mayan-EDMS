from __future__ import unicode_literals

from ..models import Tag

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL,
    TEST_TAG_LABEL_EDITED
)


class TagTestMixin(object):
    def _create_tag(self):
        self.tag = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

    def _request_tag_create_view(self):
        return self.post(
            viewname='tags:tag_create', data={
                'label': TEST_TAG_LABEL,
                'color': TEST_TAG_COLOR
            }
        )

    def _request_tag_delete_view(self):
        return self.post(
            viewname='tags:tag_delete', args=(self.tag.pk,)
        )

    def _request_tag_edit_view(self):
        return self.post(
            viewname='tags:tag_edit', args=(self.tag.pk,), data={
                'label': TEST_TAG_LABEL_EDITED, 'color': TEST_TAG_COLOR_EDITED
            }
        )
