=======
Roadmap
=======

- Other

  - Find replacement for ``cssmin`` & ``django-compressor``.
  - Find replacement for ``python-gnupg``. Unstable & inconsistent API.
  - Google docs integration. Upload document from Google Drive.
  - Get ``dumpdata`` and ``loaddata`` working flawlessly. Will allow for easier backups, restores and database backend migrations.
  - Add generic list ordering. ``django.views.generic.list.MultipleObjectMixin`` (https://docs.djangoproject.com/en/1.8/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin) now supports an ``ordering`` parameter.
  - Add support to convert any document to PDF. https://gitlab.mister-muffin.de/josch/img2pdf
  - Add support for combining documents.
  - Add support for splitting documents.
  - Add new document source to get documents from an URL.
  - Add support for metadata mapping files. CSV file containing filename to metadata values mapping, useful for bulk upload and migrations.
  - Add support for registering widgets to the home screen.
  - Merge mimetype and converter apps.
  - Metadata widgets (Date, time, timedate).
  - Datatime widget: https://github.com/smalot/bootstrap-datetimepicker
  - Add events for document signing app (uploaded detached signateure, signed document, deleted signature)
  - A configurable conversion process. Being able to invoke different binaries for file conversion, as opposed to the current libreoffice only solution.
  - A tool in the admin interface to mass (re)convert the files (basically the page count function, but then applied on all documents).
