========
Settings
========

When Mayan EDMS is initially installed a ``local.py`` file is created inside the
``/mayan/settings/`` folder. So if you installed Mayan EDMS according to the
instructions provided in this documentation your ``local.py`` should be located in
the directory: ``/usr/share/mayan-edms/mayan/settings/local.py``.

For a list of all the configuration options, go to "Setup" then "Settings" on
your browser. This is also a good place to check if your overrided setting
option value in your ``local.py`` file is being interpreted correctly.

Settings can also be changed via environment variables by prepending the string
"MAYAN_" to the configuration name. For example, to change the number of documents
displayed per page (COMMON_PAGINATE_BY, by default 40), use::

    MAYAN_COMMON_PAGINATE_BY=10
