**************
Password reset
**************

To use the password reset feature, administrative emails need to be configured.
These are sent by the system itself and not by the users. Their usage and
configuration is different than the
:doc:`email system used to share documents via email<../chapters/mailing>`.

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

To change the reference URL in the password reset emails on in the
default document mailing template modify the ``COMMON_PROJECT_URL`` setting.
For information on the different ways to change a setting check the
:doc:`../topics/settings` topic.

To test the email settings use the management command ``sendtestemail``.
Example::

    mayan-edms.py sendtestemail myself@example.com



