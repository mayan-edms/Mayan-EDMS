from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common.literals import TIME_DELTA_UNIT_DAYS

CHECK_DELETE_PERIOD_INTERVAL = 60
CHECK_TRASH_PERIOD_INTERVAL = 60
DELETE_STALE_STUBS_INTERVAL = 60 * 10  # 10 minutes
DEFAULT_DELETE_PERIOD = 30
DEFAULT_DELETE_TIME_UNIT = TIME_DELTA_UNIT_DAYS
DEFAULT_LANGUAGE = 'eng'
DEFAULT_LANGUAGE_CODES = (
    'ilo', 'run', 'uig', 'hin', 'pan', 'pnb', 'wuu', 'msa', 'kxd', 'ind',
    'zsm', 'jax', 'meo', 'kvr', 'xmm', 'min', 'mui', 'zmi', 'max', 'mfa',
    'cjy', 'nan', 'pus', 'pbu', 'pbt', 'wne', 'hsn', 'hak', 'ful', 'fuc',
    'fuf', 'ffm', 'fue', 'fuh', 'fuq', 'fuv', 'fub', 'fui', 'nep', 'npi',
    'dty', 'sin', 'khm', 'kxm', 'ell', 'grc', 'cpg', 'gmy', 'pnt', 'tsd',
    'yej', 'nya', 'mnp', 'dhd', 'cdo', 'hil', 'bcc', 'bgn', 'bgp', 'cmn',
    'kok', 'spa', 'eng', 'ara', 'por', 'ben', 'rus', 'jpn', 'deu', 'jav',
    'tel', 'vie', 'kor', 'fra', 'mar', 'tam', 'urd', 'tur', 'ita', 'yue',
    'tha', 'guj', 'fas', 'pol', 'kan', 'mal', 'sun', 'hau', 'ory', 'mya',
    'ukr', 'bho', 'tgl', 'yor', 'mai', 'uzb', 'snd', 'amh', 'ron', 'orm',
    'ibo', 'aze', 'awa', 'gan', 'ceb', 'nld', 'kur', 'hbs', 'mlg', 'skr',
    'ctg', 'zha', 'tuk', 'asm', 'mad', 'som', 'mwr', 'mag', 'bgc', 'hun',
    'hne', 'dcc', 'aka', 'kaz', 'syl', 'zul', 'ces', 'kin', 'hat', 'que',
    'swe', 'hmn', 'sna', 'mos', 'xho', 'bel'
)
DEFAULT_ZIP_FILENAME = 'document_bundle.zip'
DEFAULT_DOCUMENT_TYPE_LABEL = _('Default')
DOCUMENT_IMAGE_TASK_TIMEOUT = 120
STUB_EXPIRATION_INTERVAL = 60 * 60 * 24  # 24 hours
UPDATE_PAGE_COUNT_RETRY_DELAY = 10
UPLOAD_NEW_VERSION_RETRY_DELAY = 10

PAGE_RANGE_ALL = 'all'
PAGE_RANGE_RANGE = 'range'
PAGE_RANGE_CHOICES = (
    (PAGE_RANGE_ALL, _('All pages')), (PAGE_RANGE_RANGE, _('Page range'))
)
