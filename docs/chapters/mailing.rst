*****************
Mailing documents
*****************

Sending emails in Mayan EDMS is controlled by two different system depending on
the type of email being sent. These are administrative emails like password
reset emails and user emails sent from the application.

Sending administrative emails
=============================

To be able to send password reset emails configure the Django email settings
via the :ref:`configuration file <configuration_file>`.

Example::

    EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST: '<your smtp ip address or hostname>'
    EMAIL_HOST_PASSWORD: '<your smtp password>'
    EMAIL_HOST_USER: '<your smtp username>'
    EMAIL_PORT: 25  # or 587 or your server's SMTP port
    EMAIL_TIMEOUT:
    EMAIL_USE_SSL: true
    EMAIL_USE_TLS: false

For more details consult Django's documentation on the topic:
https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend


Application emails
==================

To allow users to send emails or documents from within the web interface,
Mayan EDMS provides its our own email system called Mailing Profiles.
Mailing Profiles support access control per user role and can use different
email backends. Mailing Profiles are created from the
:menuselection:`System --> Setup` menu.
