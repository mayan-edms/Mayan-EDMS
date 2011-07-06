from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template

from sources.staging import StagingFile

upload_document_from_local = {'text': _(u'local'), 'view': 'upload_document_from_local', 'famfam': 'drive_disk', 'keep_query': True}
upload_document_from_staging = {'text': _(u'staging'), 'view': 'upload_document_from_staging', 'famfam': 'drive_network', 'keep_query': True}#, 'condition': lambda x: USE_STAGING_DIRECTORY}
upload_document_from_user_staging = {'text': _(u'user staging'), 'view': 'upload_document_from_user_staging', 'famfam': 'drive_user', 'keep_query': True}#, 'condition': lambda x: PER_USER_STAGING_DIRECTORY}

staging_file_preview = {'text': _(u'preview'), 'class': 'fancybox-noscaling', 'view': 'staging_file_preview', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'zoom'}
staging_file_delete = {'text': _(u'delete'), 'view': 'staging_file_delete', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'delete'}

register_links(StagingFile, [staging_file_preview, staging_file_delete])

