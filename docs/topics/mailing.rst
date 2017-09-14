=================
Mailing documents
=================

To be able to send documents via email from inside Mayan EDMS you need to add
and configure the following configuration variables in your
mayan/settings/local.py file::

  EMAIL_HOST = 'smtp.gmail.com'  # Or similar
  EMAIL_PORT = 587
  EMAIL_HOST_USER = '<your smtp username>'
  EMAIL_HOST_PASSWORD = '<your smtp password>'
  EMAIL_USE_TLS = True

"Mail is sent using the SMTP host and port specified in the EMAIL_HOST and EMAIL_PORT settings. The EMAIL_HOST_USER andEMAIL_HOST_PASSWORD settings, if set, are used to authenticate to the SMTP server, and the EMAIL_USE_TLS and EMAIL_USE_SSL settings control whether a secure connection is used."

For more details consult Django's documentation on the topic: https://docs.djangoproject.com/en/1.8/ref/settings/#email-host
