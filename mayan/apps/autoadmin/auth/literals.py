from django.conf import settings

ADMIN_EMAIL_ADDRESSES = [email for name, email in settings.ADMINS]
