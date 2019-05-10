from __future__ import unicode_literals

from .literals import TEST_COMMENT_TEXT


class DocumentCommentTestMixin(object):
    def _create_test_comment(self):
        self.test_document_comment = self.test_document.comments.create(
            comment=TEST_COMMENT_TEXT, user=self._test_case_user
        )


class DocumentCommentViewTestMixin(object):
    def _request_test_comment_create_view(self):
        return self.post(
            viewname='comments:comment_add', kwargs={
                'pk': self.test_document.pk
            }, data={'comment': TEST_COMMENT_TEXT}
        )

    def _request_test_comment_delete_view(self):
        return self.post(
            viewname='comments:comment_delete', kwargs={
                'pk': self.test_document_comment.pk
            },
        )
