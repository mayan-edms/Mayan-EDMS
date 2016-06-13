from __future__ import unicode_literals

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import Tag

from .literals import TEST_TAG_LABEL, TEST_TAG_LABEL_EDITED, TEST_TAG_COLOR


class TagOrganizationViewTestCase(OrganizationViewTestCase):
    def create_tag(self):
        self.tag = Tag.objects.create(
            organization=self.organization_a, label=TEST_TAG_LABEL,
            color=TEST_TAG_COLOR
        )

    def test_tag_create_view(self):
        # Create a tag for organization A
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'tags:tag_create', data={
                    'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
                }
            )
            self.assertNotContains(response, text='danger', status_code=302)
            self.assertEqual(Tag.on_organization.count(), 1)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(Tag.on_organization.count(), 0)

    def test_tag_delete_view(self):
        # Create a tag for organization A
        self.create_tag()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post('tags:tag_delete', args=(self.tag.pk,))
            # This view redirects when no tag is available
            self.assertEqual(response.status_code, 302)

    def test_tag_edit_view(self):
        # Create a tag for organization A
        self.create_tag()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot edit the tag
            response = self.post(
                'tags:tag_edit', args=(self.tag.pk,), data={
                    'label': TEST_TAG_LABEL_EDITED
                }
            )

            self.assertEqual(response.status_code, 404)

    def test_tag_tagged_item_list_view(self):
        # Create a tag for organization A
        self.create_tag()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot find the tag for
            # organization A
            response = self.get(
                'tags:tag_tagged_item_list', args=(self.tag.pk,),
            )
            self.assertEqual(response.status_code, 404)
