import logging

from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.views.exceptions import ActionError
from mayan.apps.views.generics import MultipleObjectConfirmActionView

from ..icons import icon_favorite_document_list
from ..models.document_models import Document
from ..models.favorite_document_models import FavoriteDocument
from ..permissions import permission_document_view
from ..settings import setting_favorite_count

from .document_views import DocumentListView

__all__ = (
    'FavoriteDocumentListView', 'FavoriteAddView', 'FavoriteRemoveView'
)
logger = logging.getLogger(name=__name__)


class FavoriteDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return FavoriteDocument.objects.get_for_user(user=self.request.user)

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_favorite_document_list,
                'no_results_text': _(
                    'Favorited documents will be listed in this view. '
                    'Up to %(count)d documents can be favorited per user. '
                ) % {'count': setting_favorite_count.value},
                'no_results_title': _('There are no favorited documents.'),
                'title': _('Favorites'),
            }
        )
        return context


class FavoriteAddView(MultipleObjectConfirmActionView):
    object_permission = permission_document_view
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message = _(
        '%(count)d document added to favorites.'
    )
    success_message_plural = _(
        '%(count)d documents added to favorites.'
    )

    def get_extra_context(self):
        context = {
            'submit_label': _('Add'),
            'submit_icon': icon_favorite_document_list,
            'title': ungettext(
                singular='Add the selected document to favorites?',
                plural='Add the selected documents to favorites?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            context['object'] = self.object_list.first()

        return context

    def object_action(self, form, instance):
        FavoriteDocument.objects.add_for_user(
            document=instance, user=self.request.user
        )


class FavoriteRemoveView(MultipleObjectConfirmActionView):
    error_message = _('Document "%(instance)s" is not in favorites.')
    object_permission = permission_document_view
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message = _(
        '%(count)d document removed from favorites.'
    )
    success_message_plural = _(
        '%(count)d documents removed from favorites.'
    )

    def get_extra_context(self):
        context = {
            'submit_label': _('Remove'),
            'submit_icon': icon_favorite_document_list,
            'title': ungettext(
                singular='Remove the selected document from favorites?',
                plural='Remove the selected documents from favorites?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            context['object'] = self.object_list.first()

        return context

    def object_action(self, form, instance):
        try:
            FavoriteDocument.objects.remove_for_user(
                document=instance, user=self.request.user
            )
        except FavoriteDocument.DoesNotExist:
            raise ActionError
