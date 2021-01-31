from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    MultipleObjectDeleteView, SingleObjectDownloadView, SingleObjectListView
)

from .icons import icon_download_file_list
from .models import DownloadFile
from .view_mixins import ViewMixinRelatedObjectPermission


class DownloadFileDeleteView(
    ViewMixinRelatedObjectPermission, MultipleObjectDeleteView
):
    model = DownloadFile
    pk_url_kwarg = 'download_file_id'
    post_action_redirect = reverse_lazy(
        viewname='storage:download_file_list'
    )


class DownloadFileDownloadViewView(
    ViewMixinRelatedObjectPermission, SingleObjectDownloadView
):
    model = DownloadFile
    pk_url_kwarg = 'download_file_id'

    def get_download_file_object(self):
        return self.object.open(mode='rb')

    def get_download_filename(self):
        return force_text(s=self.object)


class DownloadFileListView(
    ViewMixinRelatedObjectPermission, SingleObjectListView
):
    model = DownloadFile

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_download_file_list,
            'no_results_text': _(
                'Download files are created as a results of a an external '
                'process like an export. Download files are retained over '
                'a span of time and then removed automatically.'
            ),
            'no_results_title': _('There are no files to download.'),
            'title': _('Downloads'),
        }
