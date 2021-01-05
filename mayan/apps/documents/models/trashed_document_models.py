from django.apps import apps

from ..managers import TrashCanManager

from .document_models import Document

__all__ = ('DeletedDocument',)


class DeletedDocument(Document):
    objects = TrashCanManager()

    class Meta:
        proxy = True

    def get_api_image_url(self, *args, **kwargs):
        """
        Override the get_api_image_url to allow trashed documents to still
        provide an URL to their first page for preview while in the trash
        can.
        """
        latest_version = self.latest_version
        if latest_version:
            first_page = self.pages.filter(enabled=True).first()

            if first_page:
                return first_page.get_api_image_url(*args, **kwargs)

    @property
    def pages_valid(self):
        """
        Override the pages_valid to allow trashed documents to still provide
        an accurate count of their pages while in the trash can.
        """
        try:
            return self.latest_version.pages.filter(enabled=True)
        except AttributeError:
            # Document has no version yet
            DocumentPage = apps.get_model(
                app_label='documents', model_name='DocumentPage'
            )

            return DocumentPage.objects.none()
