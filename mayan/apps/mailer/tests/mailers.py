from __future__ import unicode_literals

from ..classes import MailerBackend


class TestBackend(MailerBackend):
    class_path = 'django.core.mail.backends.locmem.EmailBackend'
    label = 'Django local memory backend'
