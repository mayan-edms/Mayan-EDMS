3.5.10 (2021-06-05)
===================
- Remove database transaction form the event decorator.  Solves workflows
  not being launched on document creation. Closes GitLab issue #976 and
  issue #990, thanks to users Megamorf (@megamorf), A F (@adzzzz) for the
  reports and debug information.

3.5.9 (2021-05-29)
==================
- Fix duplicated document manager scan method. Closes GitLab issue
  #974. Thanks to Nguyen Dinh Tu (@tund3010) for the report.
- Fix user model theme related field error after deleting a theme already
  assigned to a user. Closes GitLab issue #972. Thanks to Niklas Maurer
  (@nmaurer) for the report.
- Update dependency versions:

  - Django from version 2.2.20 to 2.2.23.
  - django-solo from version 1.1.3 to 1.1.5.
  - djangorestframework from version 3.11.0 to 3.11.2.
  - python-magic from version 0.4.15 to 0.4.22.

- Speed up some OCR view tests.
- Add explicit Docker logout repository during the CD/CI jobs.
- Fix permission required for the OCR content delete link to match the
  permission required for the OCR content delete view. GitLab issue #954.
  Thanks to Ilya Pavlov (@spirkaa) for the report.
- Fix permission required for the document content error list link to match
  the permission required for the document parsed content error list view.
  GitLab issue #954. Thanks to Ilya Pavlov (@spirkaa) for the report.

3.5.8 (2021-04-15)
==================
- Fix sub workflow launch state action.
- Exclude the current workflow from the sub workflow launch state action
  workflow selection form.
- Update Django from version 2.2.19 to 2.2.20.

3.5.7 (2021-03-28)
==================
- Update the sample LDAP settings file to add note about package
  version pinning required by the use of the Buster Backports.
  Closes GitLab issue #693. Thanks to Ryan Showalter (@ryanshow) for
  the report and Ilya Pavlov (@spirkaa) for a solution.
  The package list for ``MAYAN_APT_INSTALLS`` for the LDAP setting file
  is now "gcc libldap2-dev/buster-backports libsasl2-dev python3-dev".
- Update Docker base image from debian:10.7-slim to debian:10.8-slim.
- Update file caching migration 0005 to have Django generate the SQL query
  for each respective backend. Closes GitLab issue #964. Thanks to forum
  user @lsmoker for the report and research.
- Backports from version 4.0:

    - 432ec35eb7bb0b8da4765f86cb6491e7667b4831
      Ensure all tasks are properly configured. Added a check to the task
      manager app to ensure all defined tasks are properly configure in
      their respective ``queues.py`` modules.
    - Fix dynamic search task names during queue registration.
    - b883c647e943be0ef62096c456118f86ef3534ac
      1e7d85175d7379fc7dca454462497db960635e3e
      Raise object creation and edit exceptions during testing.
    - 14bdcb704269c43b8e9553aaf905e54ca7f16ced
      Don't remove arguments from overloaded .save(). Pass all arguments to
      the super class save method. Scrapping the arguments hide errors
      during testing.
    - 9fc9288b52d63aa288e430a9cc1f8fd1a4295747
      Test communication with the locking backend when the app loads.
      Add support for purging ``RedisLock`` backend locks.
      Prefix all locks in the ``RedisLock`` backend to avoid name clashing
      when using the same database.
      Ensure the default timeout setting is used by the backends.

- Move task manager app to the top of the installed apps. This ensures all
  queues are created before any other app tries to use them. Fixes the error:
  `celery.exceptions.QueueNotFound: "Queue 'default' missing from task_queues"`
- Add connectivity check for the Celery broker URL and the result backend
  settings. Closes GitLab issue #940. Thanks to Vadim Radu (@vd-rd) for the
  report.
- Update the Docker Compose file to allow specifying a different database
  host as well as a different image tag for the Mayan, PostgreSQL and Redis
  containers.
- Added the ``fuse`` package to the Docker image.
- Updated the Docker Compose file to load an env file.
- Added a default env_file with some examples uses.
- Ensure logging is available early. Move logging init to the logging app
  and move the logging app to the top of the app list.
- Backport multiple test document types code.
- Allow not updating required metadata with value. A validation was raised
  when metadata update checkbox was disable and the metadata was required.
  This behavior is now fine tuned to not raise a validation error if the
  metadata already has a value which would comply with the original purpose
  of required metadata. Closes GitLab issue #936. Thanks to Raimar Sandner
  (@PiQuer)for the report.
- Make the metadata type id usage more explicit in formsets.

3.5.6 (2021-03-14)
==================
- Port improvements from Series 3.4:
  - Update Django from version 2.2.16 to 2.2.19.
  - Optimize file caching migration 0005
  - Optimize file metadata migration 0003

- Make the ``ObjectActionMixin`` messages translatable.
- Use recent PIP to avoid installing Rust.
- Specify which PIP version to use.
- Improvements merged from series 3.3 and 3.4.

3.5.5 (2021-01-05)
==================
- Merge improvements and fixes from the 3.4 series.
- Improve the Single Page App AJAX content escape logic.
  This avoids an infinite login redirect loop on some browsers.
- Avoid self-referencing dictionaries when resolving primary key
  URL keyword arguments.
- Translation updates.
- Remove CD/CI MySQL tests. MySQL does not yet support sliced subqueries.
  This queryset paradigm is used in Mayan EDMS to avoid keeping temporary
  lists of IDs in Python memory and allow moving all queryset computation
  to the database layer. This is the cause of error 1235, "This version of
  MySQL doesn't yet support 'LIMIT & IN/ALL/ANY/SOME subquery'".
- Allow trashed documents to still display a thumbnail and accurate page
  count.
- Filter trashed documents from the active workflow and workflow states
  document lists.

3.5.4 (2020-12-14)
==================
- Document stubs without a label will now display their ID as the label.
  This allows documents without files or versions to be accessible via the
  user interface.
- Return the event type subscription list sorted by namespace label and event
  type label.
- Add icons to the mark notification as seen and mark all notification as
  seen links.
- Updated events test mixins. Allow returning one, many or all events.
- Clean up API end point enumeration API view.
- Split the misc_models.py models module into different modules.
- Stricter filtering and permission checking for duplicated documents.
  Users now need the document view permission for all duplicated documents
  for any of them to show up in the duplicated document list. The duplicate
  count column now performs filtering and will only show the count of
  duplicated documents that the user can access.
- Updated ``.get_external_object_queryset`` to ensure that the queryset is
  always up to date when the view is accessed.
- Update app views to filter trashed documents. Closes GitLab issues #910
  and #920. Thanks to Sven Gaechter (@sgaechter), Francesco Musella
  (@francesco.musella-biztems), Kevin Pawsey (@kevinpawsey), and
  None Given (@nastodon) for the reports and debug information.
- Move all static values from setting modules to the literals modules.
  Closes GitLab issue #852.
- Update workflow instance access requirements to match the intended layout
  and the current REST API layout. In order to view the list of log entries
  and the list of workflow instances of a document, the workflow permission
  view is now required for the document as well as the workflow template.
  This double permission requirement now matches the same design as the
  metadata and tags apps.
- Django's global_settings module instead of the settings module which is
  not ready at the time the default are computed.
- Add API endpoints for the workflow transition fields model.
- Add ``libarchive-zip-perl`` to the Docker image to allow EXIFTOOL to
  retrieve Zip file metadata. Closes GitLab issue #918. Thanks to Enrico
  Gargale (@egargale) for the request.
- Update Docker image from version debian:10-5 to debian:10-7.
- Switch the base image of the GitLab CI file from ubuntu 19.10 to
  debian:10-7.

3.5.3 (2020-11-11)
==================
- Ensure the document tag list view return ``DocumentTag`` instances and not
  regular ``Tag`` instances.
- Lower the severity of the ``VariableDoesNotExist`` exception when resolving
  links. This exception does not is indicative of an error in the code.
- Merge and include fixes from version 3.4.20.
- Fix column display in the dependency list views.
- Disable initial state column for workflow proxies
- Update Dropzone from version 5.4.0 to 5.7.2.
- Remove sources app custom upload form and use the app template loader.
- Remove Dropzone upload size limit.
- Increase width of the Dropzone error message box.
- Fixed an issue introduced in ``865ae60fcef38e07bbf6d09bd6032017e3603698``
  when support for adding document stubs in signal handlers was added. This
  issue causes new documents to contain two versions instead of one. The
  only consequence of this issue is extra storage usage, no data loss occurs.
  The extra document version can be safely deleted by using the document
  version revert feature. Doing this will delete the extra document version
  from the database and from the storage. Closes GitLab issue #895. Thanks
  to Lukas Auer (@lukasauer) for the report and initial investigation.

3.5.2 (2020-10-26)
==================
- Allow JavaScript from Django REST framework to be served.
  Needed for the browseable API UI.
- Merges and fixes from 3.4 series.

3.5.1 (2020-10-11)
==================
- Update xmlrpc to latest interface to fix version check view.
- Fix sources error logging interface and double logging.
- Add locking to ErrorLog to ensure only one is created per app.
- Add self healing to ErrorLog .model property to remove repeated entries.
  GitLab issue #894. Thanks to forum user @Lffy for the report.
  https://forum.mayan-edms.com/viewtopic.php?t=4027
- Fix staging folder file get_image method.
- Suppress staging folder file image tasks dependency errors on debug mode.
- Backport source link highlighting improvements from version 4.0.
- Backport support for using staging folders as sources for new document
  versions.

3.5 (2020-09-30)
================
- Update dependencies versions:

    - celery from 4.3.0 to 4.4.7
    - chart.js from 2.7.2 to 2.7.3
    - coverage from 5.0.4 to 5.1
    - coveralls from 1.11.1 to 2.0.0
    - drf-yasg from 1.6.0 to 1.17.1
    - djangorestframework from 3.7.7 to 3.11.0
    - django-extensions from 2.2.8 to 2.2.9
    - django-rosetta from 0.9.3 to 0.9.4
    - flake8 from 3.7.9 to 3.8.3
    - flex from 6.14.0 to 6.14.1
    - gevent from 1.4.0 to 20.4.0
    - graphviz from 0.13.2 to 0.14
    - ipython from 7.13.0 to 7.15.0
    - python_gnupg from 0.4.5 to 0.4.6
    - pytz from 2019.1 to 2020.1
    - safety from 1.8.7 to 1.9.0
    - select2 from 4.0.3 to 4.0.13
    - sh from 1.12.14 to 1.13.1
    - sphinxcontrib-spelling from 4.3.0 to 5.0.0
    - swagger-spec-validator from 2.4.3 to 2.5.0
    - transifex-client from 0.13.8 to 0.13.10
    - tox from 3.14.5 to 3.14.6

- Remove kombu dependency. This is automatically installed by Celery.
- Remove explicit Python 3 checks and conditional code.
- Remove conditional assignment of FileNotFoundErrorException.
  Use Python 3's FileNotFoundError.
- Remove casting of dict_type and dictionary_type.
- Add group and permission count column to the role object.
- Prefix all signals with ``signal_``.
- Move the apps search setup to their own module.
- Move the SharedUpload model to the storage app.
  The setting ``COMMON_SHARED_STORAGE`` is now ``STORAGE_SHARED_STORAGE``
  and ``COMMON_SHARED_STORAGE_ARGUMENTS`` is now
  ``STORAGE_SHARED_STORAGE_ARGUMENTS``.
- Remove usage of the python_2_unicode_compatible wrapper.
- Rename smart_settings.classes.Namespace to SettingNamespace.
- Rename smart_settings.classes.NamespaceMigration to
  SettingNamespaceMigration.
- Use headless version of Libre Office in the Docker images
  to reduce the image size.
- Remove the fragment "(object):" from all base class declarations.
- Remove settings ``DOCUMENTS_DISABLE_BASE_IMAGE_CACHE`` and
  ``DOCUMENTS_DISABLE_TRANSFORMED_IMAGE_CACHE``.
- Add keyword arguments to all the ``open()`` and ``delete()`` methods
  and functions.
- Move test related code from the common app to a new tests app.
  Test related imports from ``mayan.apps.common.tests``
  need to be renamed to ``mayan.apps.tests.tests``.
- Move compressed file related code to the storage app.
- Add new search backend based on Whoosh.
  To use it, change ``SEARCH_BACKEND`` to
  ``mayan.apps.dynamic_search.backends.whoosh.WhooshSearchBackend``.
  This backend will be the default one in a future release.
- New setting to limit the number of search results returned. This setting
  avoid runaway CPU usage on ambiguous search terms. The setting name is
  ``SEARCH_RESULTS_LIMIT`` and defaults to 100.
- Improve and unify the way icon shadows is produced. Removed the
  ``shadow_class`` and ``shadow_class_transformation_list`` arguments.
- Improve and simplify the logging system. It is now possible to change
  the level of the logging. The settings have been renamed for clarity
  and uniformity.

  The ``COMMON_AUTO_LOGGING`` and ``COMMON_PRODUCTION_ERROR_LOGGING``
  have been merged into ``LOGGING_ENABLE``.

  ``COMMON_PRODUCTION_ERROR_LOG_PATH`` is now
  ``LOGGING_LOG_FILE_PATH`` and continues to default to the
  ``MEDIA_ROOT/error.log`` path.

  The new setting ``LOGGING_LEVEL`` controls the log level.

  A second new setting named ``LOGGING_HANDLERS`` controls
  the list of output log handlers. It defaults to ``console`` but also
  supports a second one named ``logfile``. The ``logfile`` handler
  is the same one that previously enabled when setting the setting
  ``COMMON_PRODUCTION_ERROR_LOGGING`` to ``true``.
- Remove the django-test-without-migrations package.
- Split the common app into common and views. The new views app controls
  generic views, view mixins, forms, and widgets.
  The setting ``COMMON_PAGINATE_BY`` is now named ``VIEWS_PAGINATE_BY``.
- Allow access to document stubs.
- Mirroring improvements. Allow running the mountindex in the background.
  Display a message when running on the foreground to avoid confusion.
  Add internal FUSE logging and allow control of the log level.
- Move dependencies to their respective app:

  - django-mathfilters from common to templating
  - extract-msg from common to storage
  - gevent, gunicorn, whitenoise from common to platform

- Add a tags and filters selection to the template widget.
- Remove runtime.py modules and move instancing to base class.
  Avoids keeping long lived objects in memory.
- Consolidate app module loading using AppsModuleLoaderMixin.
- Remove usage of django.utils.six.
- Add django-silk as a development dependency.
  Add a development setting for django-silk.
- Add the ModelQueryFields class to allow programmatic setting
  of a model's select_related and prefetch_related fields.
  Optimize the most common queries and views to use ModelQueryFields.
- Move model error logging from the common to the new logging app.
- Generalize the model error logging code.
- Convert the user mailer and sources app to use the new logging
  app.
- Improve the logging in the sources app.
- Raise error if the watch folder doesn't exists or is not a directory.
- Support setting a limit of error log entries.
- Refactor the OCR process to use Celery canvas.
- Increase atomicity of the OCR process. GitLab issue #209.
- Disable Tesseract multi threading to speed up processing when running
  multiple instances at the same time.
- Search improvements:

  - Icons for the search, advanced search and search again links.
  - Display the search again links on empty results.
  - The search again link redirects to the same search form used instead to
    always redirect to the advanced form.

- Remove the noopocr.NoOpOCR OCR backend.
- Remove the pyocr OCR backend.
- Move the ErrorLoggingMiddleware from the common app to the logging app.
- Allow passing environment entries to the Tesseract OCR backend.
- Improve main menu styling and JavaScript code. Improve hover highlighting
  and maximize space.
- Add support for copying: document types, groups, mailing profiles,
  metadata types, messages of the day, workflows, quotas, roles, smart links,
  tags, web links.
- Add document type searches.
- Templating improvements:

  - Enable mathfilters by default.
  - Add a 'set' tag to allow setting template variables.
  - Add dict_get filter that returns a given dictionary key.
  - Add {% method %} tag to call an objects method with or without keyword
    arguments.
  - Add regular expression tags: regex_findall, regex_match, regex_search,
    regex_sub. Each regex tag supports the flags: ascii, ignorecase, locale,
    multiline, dotall, verbose.
  - Add split filter to split a value by a delimiter.

- Add workflow action to update document OCR content.
- Split TemplateField into TemplateField and ModelTemplateField.
- Split TemplateWidget into TemplateWidget and ModelTemplateWidget.
- Use TemplateField for metadata type's default and lookup fields.
- Convert the trash emptying action into a background task.
- Add support for excluding model proxies from menu link resolving via the
  .add_proxy_exclusion() menu method.
- Use proxy exclusion to disable the normal multi item document
  links from being displayed for trashed documents.
- Add subwidgets_order to NamedMultiWidget class.
- Update the statistics icon.
- Add support to change the dashboard widget details link icon.
- Fix icon for the add document to favorites link.
- Add related actions menu.
- Expose Celery's ``BROKER_LOGIN_METHOD`` and ``BROKER_USE_SSL`` via the
  new ``CELERY_BROKER_LOGIN_METHOD`` and ``CELERY_BROKER_USE_SSL`` settings.
  ``CELERY_BROKER_LOGIN_METHOD`` defaults to ``AMQPLAIN`` and
  ``CELERY_BROKER_USE_SSL`` defaults to ``None``.
- Add support for each app to specify their own static media ignore patterns
  via the app config attribute ``static_media_ignore_patterns``.
- Updated the ``static_media_ignore_patterns`` of apps to remove more unused
  media files. Lowers the static media folder size from 83MB to 51MB.
- Add boolean field to workflows to control whether or not they will launch
  when a new document is created.
- Add views to launch workflows for single or multiple documents.
- Workflow to document type matching is now enforced when launching workflows.
- Two background tasks were added to make launching workflows an asynchronous
  event. This speeds up uploading documents in bulk.
- Add the workflow action to the context of the initial state actions.
- Add multiple workflow delete view.
- Add multiple message delete view.
- Moved the statistics queue from the slow worker to the medium worker.
- Retry document page image generation tasks on lock error.
- Add settings named ``DOCUMENT_TASK_GENERATE_DOCUMENT_PAGE_IMAGE_RETRY_DELAY``
  to adjust the retry delay of the document page image generation task.
- Add workflow action to launch other workflows.
- Update the workflow action ``.get_form_schema()`` to accept the workflow state
  for which the action is being created.
- Add locking to the document page image generation to avoid a race condition
  on high load.
- Update the redactions layer to use an order of 0.
- Add decorations layer.
- Add converter assets.
- Add asset paste transformation by coordinates and by percentage.
- Add asset watermark transformation by coordinates.
- Remove transformation choices from layer model.
- Disable edit button on invalid transformations.
- Disable edit button on transformations without arguments.
- Remove transformation order field default. An empty value is more intuitive
  to the purpose of the field.
- Make transformation order column sortable.
- Group workflow actions choices by app.
- Use select2 widget for the workflow action selection field.
- Add workflow action to add transformations to document pages.
- Add support to change the Gunicorn worker class via the environment variable
  ``MAYAN_GUNICORN_WORKER_CLASS``.
- Add support for document type filename generators.
- Add themes support via the appearance app.
- Add new ``bleach`` dependency to sanitize the themes stylesheets.
- Preserve the original document filename when executing the EXIFToolDriver by
  using a temporary folder instead of a temporary file. Closes GitLab
  issue #745. Thanks to the Jeroen Van den Keybus (@vdkeybus) for the report
  and solution suggestion.
- Move mailing profile choice generation from the form to the class.
- Add "No results" text for empty file metadata driver lists.
- Add file metadata submit link for "No results" file metadata driver
  template.
- Remove converter.validators and replace it with common.validators.
- Autoimport search.py modules from apps.
- Make ``SearchField`` label optional. If not specified, the ``verbose_name``
  of the model field will be used instead.
- Sort search form fields.
- Make web link label field unique. A data migration is included to
  de-duplicate the labels before altering the schema.
- Enable the web link navigated event for subscription and as workflow
  trigger.
- Add events to assets.
- Re query search queryset after it has been sliced to workaround the ORM
  "Cannot filter a query once a slice has been taken".
- Add events to the message of the day app.
- Add search template tag to pass the search model URL and query string
  variable to the search template and avoid hardcoding it.
- Add workflow actions to add, edit, and remove metadata from documents.
- Update Docker image version from Debian 10.3 to 10.5.
- Add column to show the list of fields of a workflow transition.
- Unify the spacing of the list columns for all variations of sort columns
  and columns with help text.
- Move the column help text mark up into its own partial template.
- Only instance valid workflow transition transition fields from an
  existing workflow instance context.
- Add helper script to find missing __init__.py files.
- Trigger the workflow edited event when making changes to the workflow
  states, state actions, transitions, or transition fields.
- Update Python client for PostgreSQL from version 2.8.4 to 2.8.6, and Redis
  client version from 3.4.1 to 3.5.3.
- Initialize document version _execute_hooks with a valid result.
  Allows disabling apps that modify the hook list like document signatures.
- Do not error out when an app that defined a cached storage is
  disabled, like the workflows app.
- Disable purge method and purge links on invalid file caches.
- Do not error out when an app that defined a transformation
  layer is disabled.
- Invert the document and OCR migrations 0006 to 0003 dependency.
  Makes the OCR migration dependent on the documents app migration.
  This allows disabling the OCR app.
- Remove the transaction block when creating documents.
  This allows document stubs to be accessible from within
  signal handlers.
- Update GitLab CI Docker build and test stage to run using
  a PostgreSQL database and a Redis container.
- Remove deprecated ``BROKER_BACKEND`` setting and replace it
  with ``CELERY_BROKER_URL``.
- Default ``DEFAULT_CELERY_BROKER_URL`` to ``'memory://'``.
  This ensures operation even when there is no broker available.

3.4.22 (2021-03-13)
===================
- Update the MySQL client packages for Debian.
- Update Django from version 2.2.16 to 2.2.19.
- Optimize file caching migration 0005.
- Improvements from version 3.3.

3.4.21 (2020-12-31)
===================
- Improve the Single Page App AJAX content escape logic.
  This avoids an infinite login redirect loop on some browsers.
- Avoid self-referencing dictionaries when resolving primary key
  URL keyword arguments.
- Backport GitLab CI improvements from version 3.5.

3.4.20 (2020-11-11)
===================
- Fix REST API chapter formatting.
- Add search documentation chapter.
- Remove extra space from link label.
- Add keyword arguments to .acquire_lock().
- Add keyword arguments to shutil library usage
- Merge c18d145c4ea1d5cfb23dc8cd517bc8ddd4149782 "Generate only one CSRF
  token per HTML form" from Version 4.0.
- Merge fb3f0d3c35bf7c0880a8a4b4b650f7767ee089a7 "Merge URL and form data
  in a smarter way" from Version 4.0.

  Use URI class to merge the URL and the query string for the
  form fields in a smart way instead of just concatenating using
  a '?'.

  Closes GitLab issue #706. Thanks to Matthias Urlichs (@smurfix)
  for the report.
- Add keyword arguments to sh.Command().

3.4.19 (2020-10-26)
===================
- Fix Document indexing API view. GitLab issue #885.
- Added tests for all REST API views.
- Update GitLab CI and Make file to support automatic minor releases.
- Skip ReDoc and Swagger UI tests when using PostgreSQL to workaround Django
  issues #15802 and #27074.

3.4.18 (2020-10-22)
===================
- Update Django from version 2.2.15 to 2.2.16.
- Increase GitLab CI artifact expiration to 2 hours.
- Seed the random number generator when the test case class is initialized.
- Update test PostgreSQL makefile target to allow continuing launching
  the PostgreSQL container without password.
- Simplify and optimize file caching migration 0005_auto_20200322_0607.
- Fix the "no result" title entry of the setup item list view.
  Closes GitLab issue #900. Thanks to Matthias Löblich (@startmat) for the
  report.
- Passthrough storage improvements. Zip file is opened with the modes
  corresponding to the calling storage. New file object methods added:
  tell, write, flush, seek. Empty files when using the ``.save()`` method
  are now only created if they don't already exists. Add support to the
  encryption storage to accept unicode content. GitLab issue #876.
- Redirect to the previous view when moving document to the trash. Closes
  GitLab issue #873. Thanks to Bw (@bwakkie) for the report.
- Add the current document to the context to improve navigation in the views:
  add to favorites, remove from favorites, move to trash, delete trashed,
  and restore trashed.
- Add note for hardcoded vine dependency.
- Style fixes and missing keyword arguments.
- Add ``formset_factory`` keyword arguments.

3.4.17 (2020-09-10)
===================
- Improve and optimize the process_messages script.
- Add helper script that checks all apps have a corresponding
  Transifex resource entry.
- Update Transifex configuration file. Add missing apps, rename
  statistics to mayan_statistics to match app name, fix typo
  in web link app resource name. Thanks to forum user @qra
  (https://forum.mayan-edms.com/viewtopic.php?t=3009) for the
  report.
- Feature complete document indexing API. Forum topics 3010 and 3011.
  Thanks to forum user @qra for the reports and requests.
- Add documentation note about breaking changes in django-storages version
  1.10 regarding ``default_acl``.
- Pin vine to version 1.3.0 to workaround upstream Celery dependency breakage.
  https://github.com/celery/py-amqp/issues/340
  https://stackoverflow.com/questions/32757259/celery-no-module-named-five
  https://github.com/celery/celery/blob/v4.3.0/requirements/default.txt#L4

3.4.16 (2020-08-30)
===================
- Merge request !36 "Properly close storage file when CachePartion.create_file
  contextmanager ends". Thanks to Biel Massot (@biel.massot) for the report,
  solution, and merge request. Closes GitLab issue #870.
- Update hardware and operating system requirements.
- Expand the documentation chapter on languages. GitLab issue #831.

3.4.15 (2020-08-26)
===================
- Ensure workflow template field widgets receive an empty mapping
  when the arguments field is empty. Closes GitLab issue #862.
  Thanks to Dennis Ploeger (@dploeger) for the report, debug, and diagnostics.
- Backport events method decorator.
- Update comments app to use method event decorator. Solves forum issue in
  topic 2890. Thank to forum user @qra for the report.
- Add information about settings loading order to the settings chapter.
  Closes GitLab issue #813. Thanks to Martin (@efelon) for the report and
  debug information.
- Add API endpoint to show the valid permissions for a model.
  The URL is ``/api/objects/{app}/{model}/permissions/``.
  Forum topic 2858. Thanks to forum user @neuhs for the report.

3.4.14 (2020-08-18)
===================
- Fix resolved web link bug introduced by the commit
  79ff84f7675ba0d78b1802b9f469fc67074433a0. Thanks to forum user @qra for
  the report.
- Add web links API.
- Release file metadata lock on errors.
- Raise workflow attribute errors on DEBUG.
- Add keyword argument to parse_range.
- Remove extra spaces in ``document_signatures/storages.py`` and
  ``document_signatures/settings.py``.
- Ensure metadata default values are applied when using the REST API.
  Thanks to forum user @qra for the report and debugging.

3.4.13 (2020-08-08)
===================
- Ensure tag attach and remove events are committed when using the REST API.
  GitLab issue #850. Thanks to Olaf (@oohlaf) for the report.
- Expose the document type OCR settings model via the REST API. Closes
  GitLab issue #851. Thanks to Mike Mansell (@diamondq) for the report.
- Expose the document type parsing settings model via the REST API.
- Add keyword arguments to the any_stream function.
- Rename event_tag_remove to event_tag_removed.
- Add support to search documents and document pages by workflow transition
  comments. Closes GitLab issue #846. Thanks to Sven Gaechter (@sgaechter)
  for the report.
- Backport search app icon updates from version 3.5a1.
- Backport trashed document icon updates from version 3.5a1.
- Fix post embedded signing redirection URL.
- Update Django from version 2.2.14 to 2.2.15.
- Update Sphinx from version 3.0.3 to 3.0.4.

3.4.12 (2020-07-28)
===================
- Decode fonts dependencies when downloading. Closes GitLab
  issue #849. Thanks to Olaf (@oohlaf) for the report and
  investigation.
- Unify the delete tag view behavior.
- Update Django from version 2.2.13 to 2.2.14.
- Expose Celery settings: ``CELERY_BROKER_LOGIN_METHOD`` and
  ``CELERY_BROKER_USE_SSL``. These default to ``AMQPLAIN`` and ``None``
  respectively.

3.4.11 (2020-07-18)
===================
- Don't assume local filesystem when testing the mirroring app.
- Fix stale document instance in cascade state actions. Fixes GitLab
  issue #841. Thanks to Alexander Schlüter (@alexschlueter) for the
  report, investigation, test code, and suggested solutions.
- Wrap around long cabinet names in the document card. Fixes GitLab
  issue #843. Thanks to Will Wright (@fireatwill) for the report and
  debug information.
- Include non Mayan app translations when switching locales.
  Closes GitLab issue #848. Thanks to Frédéric Sheedy (@fsheedy) for the
  report.

3.4.10 (2020-06-24)
===================
- Fix repeated columns in the document index node list view.
- Rephrase the help text for the workflow state action and transition
  condition field.
- Switch direction of dropdowns when there is not enough area left at the
  bottom. Close GitLab issue #830. Thanks to Bw (@bwakkie) for the report.
- Minor fixes to the optional services in the default Docker compose file.
- Add support for selecting texts in cards.
- Allow passing environment entries to the Tesseract OCR backend.
- Update Sphinx from version 2.4.4 to version 3.0.3 and django-cors-headers
  from version 2.5.2 to version 3.2.1. Closes GitLab issue #835. Thanks to
  Girum Bizuayehu (@gbizuayehu) for the report.
- Allow using non unique GID and UID when starting the Docker image.
  Closes GitLab issue #834. Thanks to Alexander Schlüter (@alexschlueter)
  for the report and solution.
- Fix the storage name used in the DOCUMENTS_CACHE_MAXIMUM_SIZE callback
  function. Closes GitLab issue #838. Thanks to forum user @Obelix1981
  for the report and debug information.
- Add a dependency tracking for the graphviz dot executable used to generate
  workflow previews. It is not possible to pass a path to the graphviz Python
  library therefore this setting is only informational.
- Update Django from version 2.2.12 to version 2.2.13.
- Convert the document indexing task retry delay constant into a setting
  option. The option name is ``DOCUMENT_INDEXING_TASK_RETRY_DELAY`` and
  defaults to the previous value of 5 seconds.


3.4.9 (2020-05-26)
==================
- Add the packaging library explicitly as a dependency.
  Closes GitLab issue #825. Thanks to Martin (@efelon) for the
  report and debug information.

3.4.8 (2020-05-25)
==================
- Move django-qsstats-magic to the mayan_statistics app.
- Update Pillow from version 7.0.0 to 7.1.2.
- Update Werkzeug from version 1.0.0 to 1.0.1.
- Update devpi-server from version 5.4.1 to 5.5.0.
- Update django-celery-beat from version 1.5.0 to 2.0.0.
- Update translation files.
- Encapsulate actstream registry inside a EventModelRegistry.
- Improve default binary path detections in OpenBSD 6.7.
- Fix README link to installation chapter. Closes GitLab issue #823.
  Thanks to Matthias Löblich (@startmat) for the report.
- Add document and document version pre creation hooks.
- Use pre creation hooks to check quotas before document or document
  version creation and block user early on before
  the task is submitted.
- Wrap around long texts in the panel's body.
- Wrap around long tags when showing them in a panel's body.
- Move templating to the templating app.
- Expose Django's ``AUTHENTICATION_BACKENDS`` setting.

3.4.7 (2020-04-28)
==================
- Darken dropdown menu text to increase contrast and legibility.
- Capture and display double check in and non checked out document
  checkout attempts. Closes GitLab issue #820. Thanks to Gerald Fuchs
  (@geraldf) for the report and debug information.
- The Docker volume change owner command is now only run if there is a change
  in the UID or GID of the container's user. Merge request !81. Thanks to
  Matthias Bilger (@m42e) for the patch.
- The pip option ``--no-use-pep517`` has been removed from the installation
  and version 3.4 upgrade documents. Closes GitLab issue #810. Thanks to
  jhayn49 (@jhayn49) for the report.
- Replace self.get_object() with self.object where applicable.
- Fixed HTTP workflow action field_order. Merge request !82. Thanks to
  Matthias Bilger (@m42e) for the report and the patch.
- Add MERC 0007 defining the new repository branch layout.
- Remove outdated development version deployment instructions. Closes GitLab
  issue #821. Thanks to Gerald Fuchs (@geraldf) for the report.

3.4.6 (2020-04-19)
==================
- Update Django to version 2.2.12.
- Support custom URL base paths. Add the new setting
  ``COMMON_URL_BASE_PATH``.
- Expose Django's ``SESSION_COOKIE_NAME`` and ``SESSION_ENGINE`` settings.
- The ``checkdependencies`` command will now mark missing production
  dependencies with a symbol and an ANSI coloration.
- Add ``--csv`` option to the  ``checkdependencies`` command to output the
  result as comma delimited values.

3.4.5 (2020-04-14)
==================
- Make sure FUSE's getattr.st_size always return a 0 and not None when the
  document is invalid. Close GitLab issue #797. Thanks to telsch (@telsch)
  for the report and debug information.
- Add the Un series Korean TrueType fonts (fonts-unfonts-core) to the Docker
  image.
- Fix the document page disable and enable links. Close GitLab issue #809.
  Thanks to Kalloritis (@Kalloritis) for the report and research.
- Fix a specific scenario with the document count limit quota backend where
  a user might still be able to upload a new document past the quota limit.
- Fix typo in the document version upload URL pattern.
- Standardize the icon for returning to the document from child views.
- Move the links to return to the document from the page list, version detail
  and page image, from the facet menu to the secondary menu for proper UX
  flow.
- Fix a typo in the resolved smart link URL parameter.
- Improve resolved smart link access filtering.
- Allow apps without an urlpatterns entry.
- Update the Docker image to use Debian 10.3.
- Update the quota app to work with more deployment types.
- Add a dependency definition for the gpg binary used by the Django GPG app.
- Fix document list mode on the cabinet detail view.
- Fine tune extra small button appearance and space usage.
- Move some of the extra small button presentation from the template to the
  stylesheet.

3.4.4 (2020-04-08)
==================
- Add a custom app static media finder to workaround Django's
  AppDirectoriesFinder limitation that caused the missing
  staticfiles manifest entry error.
- Use tmpfs for gunicorn's heartbeat file under Docker. Closes GitLab issue
  #754. References: https://pythonspeed.com/articles/gunicorn-in-docker/,
  https://docs.gunicorn.org/en/latest/settings.html#worker-tmp-dir and
  https://docs.gunicorn.org/en/latest/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod

3.4.3 (2020-04-04)
==================
- Fix document page interactive transformation pages.
- Fix layer transformation selection view.
- Improve permission checking of the layer transformation
  selection view.
- Make document tag widget clickable.
- Make document cabinet widget clickable.
- Apply the ``DOCUMENTS_LIST_THUMBNAIL_WIDTH`` setting value to
  document pages and document version thumbnails too.
- Send all exception to the log system and let the log system
  perform the filtering.
- Improve the design of the 404, 403 and 500 error pages.
- Update production error log settings. Max bytes from 1024
  to 65535 and backup from 3 to 5.

3.4.2 (2020-04-02)
==================
- Fix search forms action URLs. Closes GitLab issue #802.
  Thanks to holzhannes (@holzhannes) for the report and
  debug information.
- Update document deletion message to say the documents
  were submitted for deletion and not actually deleted at
  the moment of the request.
- Detect if devpi-server is installed before building
  the Docker image.
- Re-add SQLite3 upgrade test now that the code upgrades
  from two Django 2.2 versions.
- Allow apps to inject their own head or foot templates
  to the root template.
- Added new document setting ``DOCUMENTS_LIST_THUMBNAIL_WIDTH`` to control
  the size of the thumbnails on list view mode.
- Added document head template to inject the DOCUMENTS_LIST_THUMBNAIL_WIDTH
  as a CSS style.
- Show the full path to the cabinet on cabinet search results.
- Add support for index instance search.
- Add support for search for cabinets by their document basic
  attributes.
- Add support for app passthru URL patterns.

3.4.1 (2020-04-01)
==================
- Add development setting for Docker databases.
- Add manage target against Docker databases.
- Add git-core to the Docker image to allow installing
  development Python libraries.
- Fix pre upgrade cache cleanup in file caching migration 0005.

3.4 (2020-03-30)
================
- Update Django to version 2.2.10.
- Backport list display mode. Support switching between item and list mode.
- Update app URLs to use explicit parameters.
- Move dependencies environments to their own module called
  ``dependencies.environments.py``.
- Increase the size of the file cache maximum size field.
- Add user impersonation support.
- Add support for uncompressing Outlook .msg files. Adds dependency
  ``extract-msg``.
- Updated converter to show preview of the text part of .msg files.
- Decouple the Checkouts and Sources apps. It is now possible to disable
  the Checkouts app.
- Add new document version pre save hooks.
- Fix OCR model property.
- Add workflow transition conditionals.
- Add workflow state action conditionals.
- Add document version pre save signal.
- Update the document type and document models to avoid a double save
  when creating a new document.
- Add quotas app.
- Add support for HTTP methods to the workflow HTTP request state action.
- Add the trash document workflow state action.
- Add support for GPG backends. Add two new settings ``SIGNATURES_BACKEND`` and
  ``SIGNATURES_BACKEND_ARGUMENTS``. This change also removes two settings:
  ``SIGNATURES_GPG_HOME`` and ``SIGNATURES_GPG_PATH``. ``SIGNATURES_GPG_HOME``
  had already been deprecated and was innactive. ``SIGNATURES_GPG_PATH`` is now
  component ``gpg_path`` of the setting ``SIGNATURES_BACKEND_ARGUMENTS``.
- Add sane default paths for the GPG binary for Linux, FreeBSD, OpenBSD, and
  MaCOS.
- Refactor the search app to support backends. Adds two new settings:
  ``SEARCH_BACKEND`` (which defaults to ``mayan.apps.dynamic_search.backends.django.DjangoSearchBackend``)
  and ``SEARCH_BACKEND_ARGUMENTS``.
- Update interface of the CompressedStorage backend.
- Add defined storage class.
- Convert the file caching app to used defined storage.
- Show percentage of usage for file caches.
- Add Passthrough storages.
- Add encrypted storage backend.
- Add compressed storage backend.
- Add management command to process storage.
- Automatic storage module loading.
- Convert file caching app to use defined storage.
- Removed a possible race condition when returning the signature of just
  signed document using embedded signatures.
- Updated version of the development and documentation dependencies.
- Execute the ``preparestatic`` as part of the ``initialsetup`` and
  ``performupgrade`` commands.
- Detect redirect loops when attempting to escape the AJAX container.
- Improve icons of the OCR, file metadata, and document parsing apps.
- Detect is a SourceColumn can be made sortable.
- Update python-gnupg from version 0.3.9 to 0.4.5.
- Update Django stronghold to version 0.4.0.
- Update Python libraries versions: Python Redis version from 3.3.11 to 3.4.1,
  PyYAML from 5.1.2 to 5.3.1, django-formtools from 2.1 to 2.2,
  django-mathfilters from 0.4.0 to 1.0.0, django-model-utils from 3.1.2 to
  4.0.0, django-mptt from 0.9.1 to 0.11.0, django-qsstats-magic from
  1.0.0 to 1.1.0, django-widget-tweaks from 1.4.5 to 1.4.8, furl from 2.0.0
  to 2.1.0, gunicorn from 19.9.0 to 20.0.4, mock from 2.0.0 to 4.0.2,
  pycountry from 18.12.8 to 19.8.18, requests from 2.21.0 to 2.23.0,
  whitenoise from 4.1.4 to 5.0.1, devpi-server from 5.4.0 to 5.4.1,
  Pillow from 6.2.2 to 7.0.0, node-semver from 0.6.1 to 0.8.0, graphviz from
  0.10.1 to 0.13.2, python-dateutil from 2.8.0 to 2.8.1, flanker from 0.9.0
  to 0.9.11, django-activity-stream from 0.7.0 to 0.8.0.
- Removal of Python library django-timezone-field.
- Remove codecov dependency.
- Remove pathlib2 dependency, it is now part of the standard Python library.
- Remove Django's admindocs app

3.3.18 (2021-03-13)
===================
- Optimize file metadata migration 0003.
- Update Transifex client to version 0.13.7.
- Specify which PIP version to use.
- Use recent PIP to avoid installing Rust.
- Backport GitLab CI improvements.
- Backport Makefile improvements.

3.3.17 (2020-04-09)
===================
- Removed a possible race condition when returning the signature of just
  signed document using embedded signatures.
- Add development setting for Docker databases.
- Add manage target against Docker databases.
- Use tmpfs for gunicorn's heartbeat file under Docker. Closes GitLab issue
  #754. References: https://pythonspeed.com/articles/gunicorn-in-docker/,
  https://docs.gunicorn.org/en/latest/settings.html#worker-tmp-dir and
  https://docs.gunicorn.org/en/latest/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod
- Update contributed LDAP setting file.
- Improve the design of the 404, 403 and 500 error pages.
- Update production error log settings. Max bytes from 1024
  to 65535 and backup from 3 to 5.
- Detect if devpi-server is installed before building
  the Docker image.
- Add git-core to the Docker image to allow installing
  development Python libraries.
- Send all exception to the log system and let the log system
  perform the filtering.
- Add development setting for Docker databases.
- Add manage target against Docker databases.
- Copy minor improvements to the default Docker Compose file.

3.3.16 (2020-03-17)
===================
- Fix minor release notes typographical errors.
- Update psutil from version 5.6.3 to 5.7.0. CVE-2019-18874
  (https://nvd.nist.gov/vuln/detail/CVE-2019-18874)
- Update python-gnupg from version 0.3.9 to 0.4.5. CVE-2019-6690
  (https://nvd.nist.gov/vuln/detail/CVE-2019-6690)
- Update django from version 1.11.28 to 1.11.29. CVE-2020-9402
  (https://nvd.nist.gov/vuln/detail/CVE-2020-9402)
- Decrease the code and data inside the transaction. Removes a file caching
  creation from inside a database transaction. Attempted fix for
  GitLab issues #782 and #735.
- Fix OCR model property. It was listed as document.content instead of
  document.ocr_content.
- Revert an API permission change for the EventList API view.
  Fixes GitLab issue #794. Thanks to Matthew Grady (@FlowerCoffeeCup)
  for the report and investigation.

3.3.15 (2020-03-05)
===================
- Add Docker environment setting ``MAYAN_SKIP_CHOWN_ON_STARTUP`` to skip
  performing the initial chown on the media folder at `/var/lib/mayan`.
  This command is slow on non native block storage backends.
- Remove Wiki links from README files. GitLab Merge request !78.
  Thanks Steffen Raisin (@zintor) for the merge request.
- Add more API tests to the Tags app.
- Expose Django settings: ``SECURE_PROXY_SSL_HEADER``,
  ``USE_X_FORWARDED_HOST``, and ``USE_X_FORWARDED_PORT``.
- Change the default of DATABASE_CONN_MAX_AGE to 0 which is the
  safest value. https://docs.djangoproject.com/en/3.0/ref/settings/#conn-max-age
- Update default Docker Compose file.
- Correct the icon used for multi document cabinet add action.
  GitLab merge !79. Thanks to  Giacomo Catenazzi (@cateee).
- Add environment variable ``MAYAN_DOCKER_WAIT`` to have the Docker image
  wait for a host and port to become available.
- Turn hard-coded constant STUB_EXPIRATION_INTERVAL into a user setting named
  ``DOCUMENTS_STUB_EXPIRATION_INTERVAL``. Defaults to previous value of 24
  hours to preserve existing behavior.

3.3.14 (2020-02-23)
===================
- Add missing backslash in deployment instructions.
  Closes GitLab issue #780. Thanks to Steve Palmer (@steverpalmer)
  for the report.
- Update CI script to push multiple tags.
- Remove Wiki link in the about view.
- Remove social media links.
- Add support link.
- Add more expressive error message when an invalid storage argument
  setting is encountered.
- Make document language field a lazy field. This allows starting Mayan
  even when there are invalid language codes in the DOCUMENTS_LANGUAGE_CODES
  setting.
- Warn about invalid document language codes in the DOCUMENTS_LANGUAGE_CODES
  setting. Thanks to forum user @j_arquimbau for the report.
- Add complete staging folder and staging folder file REST API. Closes GitLab
  issue #778. Thanks to David Kowis (@dkowis) for the request.
- Add the selenium Firefox geckodriver to the setup-dev-environment target.
- Move the ``purgeperiodictasks`` command to the task manager app.
- Remove left over ``interactive`` option usage for the ``purgeperiodictasks``
  command. Closes GitLab issue #785. Thanks to Matthias Löblich (@startmat)
  for the report.
- Exclude ``/favicon.ico`` from the authenticated URL list. Closes GitLab
  issue #786. Thanks to Matthias Löblich (@startmat) for the report.
- Rename test document creation method for clarity.

3.3.13 (2020-02-14)
===================
- Update management command interface. Subclasses of BaseCommand no longer
  have an 'interactive' option.
- Update usage of is_authenticated as it is now only a property. This is
  recommended for Django 1.11 and will be required in Django 2.0.
- Convert URL to string before redirect in the sources app wizard.
  Recommend for Django 1.11 and required for Django 2.0.
- Update Django to version 1.1.28
  (https://docs.djangoproject.com/en/3.0/releases/1.11.28/)
- Prioritize Mayan's translations over Django's built in ones.
  Fixes GitLab issue #734. Thanks to Roberto Novaes (@rvnovaes)
  for the report.
- Add make file target to remove fuzzy translation markers.
- Move the language files for the Bosnian language from
  the bs_BA locale to the bs locale.
- Move the language files for the Slovenian language from
  the sl_SI locale to the sl locale.
- Move the language files for the Vietnamese language from
  the vi_VN locale to the vi locale.
- Move the language files for the Dutch language from
  the nl_NL locale to the nl locale.
- Move the language files for the Danish language from
  the da_DK locale to the da locale.
- Add make file target to cleanup source translation files.
- Cleanup minor but frequent translation files issues accumulated by the
  automatic tools. Many new text string are now available for translation.
- Update the doToastrMessages to avoid appending new style updated
  indefinitely on list sort updates. Closes GitLab issue #772. Thanks
  to Matthias Löblich (@startmat) for the report and debug information.

3.3.12 (2020-02-10)
===================
- Fix issue with the template object count logic introduced in the
  last optimization.
- Fix Chinese translation. Locale cn has been renamed to cn-hans.

3.3.11 (2020-02-07)
===================
- Fix document preview rendering issue introduced by the read only
  decimal field display addition. Closes GitLab issue #771.
  Thanks to Christoph Roeder (@brightdroid) for the report and
  investigation.
- Add message about decompression bomb DOS attacks. Add mention
  how to disable the protection by increasing the allowed image
  size.
- Optimize lists title item count calculations.
- Fix document properties form default language selection. Closes GitLab
  issue #770. Thanks to Albert ARIBAUD (@aaribaud) for the report and
  for narrowing down the cause.
- Add document language codes settings tests. Closes GitLab issue #547.
  Thanks to Bebef (@Bebef) for the report and research.
- Move the django.contrib.admindocs to be loaded after the Tags app
  to avoid its translations to take precedence. Closes GitLab issue #734.
  Thanks to Roberto Novaes (@rvnovaes) for the report.

3.3.10 (2020-01-31)
===================
- Turn TarArchiveClassTestCase in to reusable archive test case class.
  #MD-10.
- Add test runner option for testing excluded tests.
- Add data operation to file metadata 0002 to remove duplicated entries.
  Closes GitLab issue #762. Thanks to forum user benaser for the report.
- Add package django_migration_test and add migration test to the
  file metadata app for migration 0002.
- Update make file to remove repeated commands and add migration testing
  target.
- Update the GitLab CI file to use the test makefile target and add
  migration testing.
- Update the Docker run_tests command to perform migration testing.
- Update translation files.
- Add support for specifying related fields per model to the templating
  app.
- Add grouping to the templating widget. Model attributes are now group
  into model properties, models fields and the new model related fields.
- Add document OCR content and parsed content as document model properties
  for use in templates.
- Fix the staging folder file API views. GitLab issue #764. Thanks to
  David Kowis (@dkowis) for the report, debug, and research.
- Add command to show the current version of Mayan. The command is named
  ``showversion``. The command has one option `--build-string`` that will
  show the build string instead. Closes #MD-14.
- Add command to check if the current version is the latest one. The command
  is named ``checkversion``. Closes issue #MD-28.
- Add button to launch a specific workflow for existing documents.
  Issue #MD-171.
- Update Pillow to version 6.2.2.
- Improve image page count detection by capturing undocumented Pillow
  exception. Close GitLab issue #767. Thanks to Frédéric Sheedy (@fsheedy)
  for the report, debug information, and test image.
- Add new setting to disable the API documentation links from the tools menu.
  The setting is named ``REST_API_DISABLE_LINKS`` and defaults to ``false``.
- Add new setting to disable the password reset link in the login form. This
  link is not used for third party authentication such as when using LDAP.
  The setting is named ``AUTHENTICATION_DISABLE_PASSWORD_RESET`` and
  defaults to ``false``.
- Improve workflow app navigation.
- Add fall back read-only render for form fields.

3.3.9 (2020-01-18)
==================
- Update Document and Lock models to avoid triggering a new migrations on
  default document language change and on default lock timeout change.
  Closes GitLab issue #759.
- Cleanup repository top level. Moved helper scripts to contrib/scripts.
- Add makefile target to make it easier to create the code coverage report.
- Remove unused Magnum and Travis CI files.
- Add makefile target to run GitLab CI jobs locally.
- Add GitLab CI jobs to test upgrading from current to newest version.

3.3.8 (2020-01-17)
==================
- Update literals so the correct paths of pdfinfo, pdftoppm, libreoffice,
  exiftool and tesseract are found. Relates to Gitlab issue #308
- Fix document detached signing. Closes GitLab issue #732.
  Thanks to holzhannes (@holzhannes) for the report and debug information.
- Updated direct deployment documentation to advise users installing
  in a custom directory to verify the automatically generated
  supervisor configuration file. Addresses GitLab issue #739
- Added a note to the LDAP section of the FAQ to assist users with
  potential local environment issues
- Updated docker-compose.yml and documentation to ensure RabbitMQ messages
  are persistent
- Improve the File Storage section of the Documentation
- Add support and documentation for S3 storage backend
- Update documentation push CI stage to delete existing files before
  uploading new content. GitLab issue #721. Thanks to Chris Whitten
  (@whit1206) for the report.
- Ensure that the model property choice field of the template widget
  is never required, regardless of the required setting of the template
  field. GitLab issue #748. Thanks to forum user chrimpshrine for the
  report.
- Remove repeated raise statement that cause HTML markup to show on
  upload error display.
- Improve file metadata property label.
- Improve file metadata property path reading. Will not error out
  when passed invalid path to the driver as reference.
- Make the sandbox template field a required field.
- Fix Tag apps API required permissions. The required permissions
  of the API match those of the view and comply with MERC 0006.
- Fix metadata app view permissions layout. The metadata add, edit, and
  remove permissions are now required for both the document and the
  the metadata type in order to add, edit or remove a metadata from
  a document. The HTML and API were updated, as well as the document
  metadata widget to only show metadata types for which the document
  metadata view permission is granted.
- Initialize permissions on every start or installation instead of
  them being initialized on demand. Closes GitLab issue #757.
  Thanks to forum user Roberto Novaes (rvnovaes) for the report.
- Add new entry to the CONVERTER_GRAPHICS_BACKEND_ARGUMENTS setting to
  allow passing a maximum image pixel count to Pillow. The entry
  is called 'pillow_maximum_image_pixels' and defaults to 89478485.
- Fix document metadata add, edit, and remove redirects.

3.3.7 (2019-12-31)
==================
- Use Python Redis client 3.3.11 to enable .client() method for the Redis
  lock backend. Add version check to the Redis lock backend. GitLab
  issue #719. Thanks to Rob de Canha-Knight (@rssfed23) for the report and
  research.
- Run Selenium tests in headless mode.
- Remove repeated document tags preview column.
- Remove cabinet links from the document cabinet list view.
- Enable display of MissingItem class instances.
- Add tests for the common.http.URL class.
- Update FAQ and troubleshooting chapters.
- Update Docker installer, sample docker-compose file and documentation to
  add a password to the Redis container. GitLab issue #712. Thanks to
  Matthew Thode (@prometheanfire) for the report.
- Use a fake config file during tests.
- Update Django to version 1.11.27.
- Add password to the Redis container for the staging Docker targets.
- Add new test case BaseTransactionTestCase.
- Improve file metadata driver database registration. Improve indexing
  based on file metadata properties. Improves GitLab issue #720 on the
  signal commit side of the indexing. Thanks to Rob de Canha-Knight
  (@rssfed23) for the report and debug information.
- Replicate transaction handling improvements from the file metadata app to
  the OCR and document parsing apps.
- Initialize indexes in a predictable way. Solves GitLab issue #720 Thanks
  to Rob de Canha-Knight (@rssfed23) for the report and debug information.
- Make file metadata StoredDriver fields unique. Relates to GitLab issue #720
  Thanks to Rob de Canha-Knight (@rssfed23) for the report and debug
  information.
- Fix the POP3 source under Python 3. GitLab issue #724. Thanks to Kevin
  Pawsey (@kevinpawsey) for the report and debug information.
- Merge NFS troubleshooting section. Thanks to Rob de Canha-Knight
  (@rssfed23). GitLab merge !67.
- Improve mirroring code to support slashes in index node values and document
  labels and also support duplicate nodes values or documents labels. Slashes
  are replaced with underscores. To handle duplicates, the primary key of
  the object is appended to the label inside parenthesis. Closes
  GitLab issue #722. Thanks to Rob de Canha-Knight (@rssfed23) for the
  report and research.
- Fix workflow document signing action. Also add message when trying to use
  action for an initial state when the created document has no version
  associated. GitLab issue #726. Thanks to forum user @holzhannes for the
  report.

3.3.6 (2019-12-19)
==================
- Make list toolbar stick to the top of the view when scrolling.
- Fix page count on some PDF files, and fix a Python 3 incompatibility.
  GitLab merge !64. Thanks to O2 Graphics (@O2Graphics).
- Improve the executables paths on FreeBSD/OpenBSD. GitLab merge !63.
  Thanks to O2 Graphics (@O2Graphics).
- Fix document orientation detection. GitLab issue #713. Thanks to
  Rob de Canha-Knight (@rssfed23) for the report and debug information.
- Update the Redis lock connection initialization so that is works with Redis
  versions < 5.0. GitLab issue #709. Rob de Canha-Knight (@rssfed23) for the
  report and debug information.
- Update the ZipArchive class to work with badly encoded filenames.
  GitLab issue #651. Thanks to Fabian (@ruffy91) for the report.
- Delete periodic task on document type delete. Closes GitLab
  issue #715. Thanks to Rob de Canha-Knight (@rssfed23) for the
  report and research.
- Add transaction handling to the interval sources delete and save
  methods.
- Add support for functional tests using selenium. Use TEST_SELENIUM_SKIP
  to skip these tests.
- Add test for issue #494.
- Add support for configurable test view template.
- Add support for public test views.
- Reapply fix for issue #494. To avoid exploit of cross site scripting in
  login view. Thanks to the Checkmarx SCA AppSec team for the research
  regarding this issue for the recent version and thanks to Lokesh
  (@lokesh1095) for the original report and solution. GitLab issue #494.
- Settings: Display overridden instead of overrided.
  GitLab merge !65. Thanks to Rob de Canha-Knight (@rssfed23).
- Update the address of PyPI when checking for new versions to avoid
  SSL errors from reusing the old address (pypi.python.org/pypi)
  certificate. GitLab issue #717. Thanks to Jordan Wages (@wagesj45)
  for the report.
- Allow passing TEST_SELENIUM_SKIP as an environment variable.
- Skip Selenium tests inside the Docker container.

3.3.5 (2019-12-13)
==================
- Pin django-timezone-field to version 3.1. GitLab issue #698.
  Thanks to Rob de Canha-Knight (@rssfed23) for the report
  and research.
- Pin kombu to version 4.6.7. GitLab issue #699. Thanks to
  Rob de Canha-Knight (@rssfed23) for the report and the research.
- Update instances of the word "weblink" to "web link".
- Unify the creation of the temporary config file used in tests.
- Update all 0001 setting migrations to accept manually migrated
  settings.
- Update TemplateField to concatenate existing help texts.
- Don't show the edit and delete links for resolved web links.
- Exclude Smart link setup columns and links from the resolved
  smart link views.
- TemplateField shows the available variable in the help text
  automatically.
- Use TemplateField for the web link template.
- Use TemplateField for smart links.
- Add the ID and the URL to the checkout serializer.
- Add BaseTransformationType metaclass in a way compatible with
  Python 2 and Python 3.
- Remove Django DownloadView library. Implement downloads natively
  using a modified port of Django 2.2 FileResponse.
- Increase the role label field size from 64 to 128 characters.
- Increase the smart link label size from 96 to 128 characters.
- Increase the source label field size from 64 to 128 characters.
- Add missing link icons.
- Add missing field help texts.

3.3.4 (2019-12-09)
==================
- Update the gunicorn worker class to synchronous.
- Update the way the BaseTransformationType metaclass is passed
  to work on Python 3.
- Add locking to the file metadata document processing task.
- Update devpi-server version to 5.3.1.
- Add targets to run staging containers using RabbitMQ as
  broker.
- Don't set SourceColumn to the attribute name when no help text
  is defined.
- Make it clear when a setting is being overridden by an environment
  variable. Add better text explanation. Change the column to a check
  mark widget.
- Add icons to the smart settings links.
- Fix docker-runtest-all target.
- Fix the evaluation priority of the bootstrap settings. Closes GitLab issue
  #702. Thanks to Kevin Pawsey (@kevinpawsey) for the report and the help
  debugging the issue.
- Switch from librabbitmq to py-amqp. Closes GitLab issue #699. Thanks to
  Rob de Canha-Knight (@rssfed23) for the report, research, and debug.
- Darken content area when opening the mobile menu.

3.3.3 (2019-12-05)
==================
- Fix transformation label display in transformation create view.
- Remove supervisor environment variable expansion.
- Don't exit GitLab makefile target if the branch to delete doesn't exist.
- Automatically create transformations from the selection form that
  doesn't have arguments.
- Add missing message displays for transformation error creation and
  not argument transformation creation.
- Mark missing text for document indexing as translatable.

3.3.2 (2019-12-05)
==================
- Improve setting migration method matching. Avoid executing
  a migrations for settings with similar but shorter names.
- Fix sources app setting migrations.
- Add OCR app setting migrations.
- Improve upgrade and deployment instructions.
- Update backup chapters to refer to upstream database documentation.

3.3.1 (2019-12-04)
==================
- Update Celery broker environment variable in the docker installer.
- Add preparestatic command to documentation. GitLab issue #692.
  Thanks to Christopher S. Meiklejohn (@cmeiklejohn2) for the report.
- Add sources setting migration.
- Savesettings command fixes.
- Fix username color on mobile screens.
- Hide the multi item selection help text on mobile screens.
- Update Django to version 1.11.26.
- Remove body spacer HTML and JavaScript. Not needed with the new UI.
- Change the required permission to view the document parsing error
  from "View document parsed content" to "Parse document". This way only
  users with the access to affect the parsed content are the only ones
  that can view what errors occurred during parsing.

3.3 (2019-12-03)
================
- Add support for icon shadows.
- Add icons and no-result template to the object error log view and
  links.
- Use Select2 widget for the document type selection form.
- Backport the vertical main menu update.
- Backport workflow preview refactor. GitLab issue #532.
- Add support for source column inheritance.
- Add support for source column exclusion.
- Backport workflow context support.
- Backport workflow transitions field support.
- Backport workflow email action.
- Backport individual index rebuild support.
- Rename the installjavascript command to installdependencies.
- Remove database conversion command.
- Remove support for quoted configuration entries. Support unquoted,
  nested dictionaries in the configuration. Requires manual
  update of existing config.yml files.
- Support user specified locations for the configuration file with the
  CONFIGURATION_FILEPATH (MAYAN_CONFIGURATION_FILEPATH environment variable),
  and CONFIGURATION_LAST_GOOD_FILEPATH
  (MAYAN_CONFIGURATION_LAST_GOOD_FILEPATH environment variable) settings.
- Move bootstrapped settings code to their own module in the smart_settings
  apps.
- Remove individual database configuration options. All database
  configuration is now done using MAYAN_DATABASES to mirror Django way of
  doing atabase etup.
- Added support for YAML encoded environment variables to the platform
  templates apps.
- Move YAML code to its own module.
- Move Django and Celery settings.
- Backport FakeStorageSubclass from versions/next.
- Remove django-environ.
- Support checking in and out multiple documents.
- Remove encapsulate helper.
- Add support for menu inheritance.
- Emphasize source column labels.
- Backport file cache manager app.
- Convert document image cache to use file cache manager app.
  Add setting DOCUMENTS_CACHE_MAXIMUM_SIZE defaults to 500 MB.
- Replace djcelery and replace it with django-celery-beat.
- Update Celery to version 4.3.0
  Thanks to Jakob Haufe (@sur5r) and Jesaja Everling (@jeverling)
  for much of the research and code updates.
- Support wildcard MIME type associations for the file metadata drivers.
- Update Gunicorn to use sync workers.
- Include devpi-server as a development dependency. Used to speed up
  local builds of the Docker image.
- Update default Docker stack file.
- Remove Redis from the Docker image. A separate container must now
  be deployed.
- Add Celery flower to the Docker image.
- Allow PIP proxying to the Docker image during build. Can be used
  with the local devpi-server or other similar.
- Default Celery worker concurrency to 0 (auto).
- Set DJANGO_SETTINGS_MODULE environment variable to make it
  available to sub processes.
- Add entrypoint commands to run single workers, single gunicorn
  or single celery commands like "flower".
- Add platform template to return queues for a worker.
- Update the EXIFTOOL driver to run for all documents
  regardless of MIME type.
- Remove task inspection from task manager app.
- Move pagination navigation inside the toolbar.
- Remove document image clear link and view.
  This is now handled by the file caching app.
- Add web links app.
- Add support to display column help text
  as a tooltip.
- Update numeric dashboard widget to display
  thousand commas.
- Add support for disabling document pages.
- Add support for converter layers.
- Add redactions app.
- Unify all line endings to be Linux style.
- Add support for changing the system messages position.
  GitLab issue #640. Thanks to Matthias Urhahn (@d4rken).
- Update Docker deploy script. Use alpine postgres version.
  Support Docker networks and make it the default.
  Delete the containers to allow the script to be idempotent.
  Deploy a Redis container.
- Improve document version upload form.
- Use dropzone for document version upload form.
- Allow the "Execute document tools" permission to be
  granted via ACL.
- Update IMAP source to be UID based.
- Add support for custom IMAP search criteria.
- Add support for executing custom IMAP STORE commands
  on processed messages.
- Add support to execute the IMAP expunge command after each
  processed message.
- Add support for specifing a destination IMAP mailbox for
  processed messages. GitLab issue #399. Thanks to
  Robert Schöftner (@robert.schoeftner).
- Support simple search disable via the new
  SEARCH_DISABLE_SIMPLE_SEARCH setting.
- Move all generic API classes definitions to the
  rest_api.generics module.
- Update API status code on insufficient access for the apps:
  indexes, parsing, documents, metadata, ocr, permission,
  user management.
- Split document app links.
- Make Postgres container wait delay configurable.
- Enable the sidebar workflow runtime link when
  the workflow view permission is granted to at
  least one workflow.
- Add ACL support to smart links.
- Add "no result" template to staging folder files
  view.
- Split duplicated document views, links into their
  own module.
- Update label and icon of the document sign form
  Label updated from "Save" to "Sign".
- Document signatures API views.
- Add and improve document signatures app tests.
- Rename document_states/tests/test_workflow_actions.py to
  document_states/tests/base.py.
- Added TestServerTestCaseMixin to perform mocked HTTP
  requests.
- Authentication and headers added to the workflow
  HTTP POST action.
- Update the timeout field of the workflow HTTP POST
  action to support templates. The timeout field also
  support integers, float, or empty values.
- DjangoSMTP mailer password field size increased to 192
  characters.
- Improve TestModelTestMixin. Allow specifying a base model.
  Fix passing the dynamic Meta class to the test model.
- Support for proxy model permission inheritance. Proxy models
  now get the permission inheritance from their base models.
- Update common.http.URL to allow passing a query dictionary.
- Add the document template sandbox feature.
- Use the generic TemplateField for the expression field
  of index tree templates.
- Add document trashed event. Closes GitLab issue #608
  Thanks to Vikas Kedia (@vikaskedia) for the report.
- Add transaction handling to document model events.
- Add back support for individual database settings
  for compatibility with version 3.2 settings.
  These are now a fallback if the new 'DATABASES'
  setting is not specified.
- Refactor the initial setting bootstrap code.
- Use timezone aware date for document statistics
- Show placeholder label on invalid action classes
  Instead of throwing an error a sample label of
  "Unknown action type" will be used and allow users to
  delete the unknown state action.
- Add workflow action to sign documents.
- Support running specific tests inside the Docker container.
  docker run --rm mayanedms/mayanedms:3.3 run_tests
- Make the statistics slug field unique.
- Self-heal statistics results model when multiple
  results are created using the same slug value.
  Forum topic 1404.
- Add "run_command" Docker entrypoint option to run arbitrary
  Mayan management command.
- Allow specifying the queue list for the run_worker Docker
  command.
- Switch default installation to use two Redis
  databases. One for the message broker, and the
  other to store task results.
- Complete the prefixing of template tags with the
  app name.
- Remove unused template tags.
- Add support for setting migrations.
- Add setting migrations for the common, converter, documents,
  file metadata, and document signatures app.
- Add document type change API endpoint.
- Change OCR API submit URL from documents/{pk}/submit
  to documents/{pk}/ocr/submit.
- Add Redis based distributed lock backend. Requires one
  argument: "redis_url". Example: redis://127.0.0.1:6379/0
- Add the setting LOCK_MANAGER_BACKEND_ARGUMENTS.
- Automate documentation building dependencies.
- Add sphinx sitemap extension.
- Move the file patching code from the Dependency class to a
  generalized utility of the storages app.
- Add book link to the documentation.
- Update mayan_statistics migration 0002 to rename
  duplicate slugs.
- Add document index reset view.

3.2.12 (2019-XX-XX)
===================
- Add Mayan container port environment variable to the
  docker installer. Thanks to Sergios Kefalas for the patch.
- Fix off-by-one error in document statistics.

3.2.11 (2019-11-28)
===================
- Backport transaction handling to document model events.
- Update example LDAP authentication settings file.
- Update FAQ entry about the LDAP file.
- Automate documentation building dependencies.
- Add sphinx sitemap extension.
- Move the file patching code from the Dependency class to a
  generalized utility of the storages app.
- Add book link to the documentation.
- Make the statistics slug field unique.
- Self-heal statistics results model when multiple
  results are created using the same slug value.
  Forum topic 1404.
- Update mayan_statistics migration 0002 to rename
  duplicate slugs.
- Fix reverse inheritance permissions.
- Remove index create permission as an ACL permission
  for indexes.
- Fix API example.
- Fix document check in via the API. GitLab issue #688.
  Thanks to inam ul haq (@inam.sys) for the report.
- Improve supervisord upgrade instructions. Forum topic 880.

3.2.10 (2019-11-19)
===================
- Auto-import dependencies. No need to use:
  from .dependencies import *  # NOQA
- Add makefile target to run all tests in debug mode.
  This mode is more strict and sidesteps a Django bug that
  causes errors in the template code that to be silent during
  tests.
- Rename expected_content_type to expected_content_types
  and allow a list of content types to be specified.
- Add missing label to metadata and file metadata model
  properties entries.
- Improve workflow field help text. Make it usable
  for the creation/edit form help text and for the
  column pop over.
- Fix NamedMultiWidget issue on Python 3. Affects
  document checkout form. GitLab issue #683. Thanks
  to John Bentley (@johnbentleyii) for the report.
- Add missing Event class cache invalidation when
  calling the refresh() method.
- Use timezone aware date for document statistics.
- Show placeholder label on invalid action classes
  Instead of throwing an error a sample label of
  "Unknown action type" will be used and allow users to
  delete the unknown state action.
- Automate paths in documentation.
- Settings chapter improvements.
- Documentation paths consistency fixes.
- Expand custom Python setting section.

3.2.9 (2019-11-03)
==================
- Move IMAPMockServer to its own module.
- Display feedback message when testing a mailing profile.
- Add tests to the platform app.
- Fix platformtemplate command --context option help message.
- Language translations update.
- Add target to run all translations targets.
- Backport color log formatter from branch version/next.
- Don't raise error checking AnonymousUser for permissions.
  Instead return always False.
- Enable the main menu workflow runtime link when the workflow view
  permission is granted to at least one workflow.
- Make Postgres container wait delay configurable. GitLab issue #677.
  Thanks to Antenore Gatta (@antenore) for the report.
- Update Django to version 1.11.25.
- Update PyYAML to version 5.1.2.
- Update celery to version 3.1.26.post2.
- Update django-celery to version 3.2.2.
- Update pathlib2 to version 2.3.5.
- Update whitenoise to version 4.1.4.
- Update Pillow to version 6.2.1.
- Move Celery and Django Celery dependencies
  to the task manager app.
- Improve dependecies app tests.
- Return st_nlink of 1 files in mirrored indexes. GitLab issue #676.
  Thanks to Ezio Vernacotola (@eziove) for the report and solution.
- Fix MAYAN_GUNICORN_TIMEOUT Docker image setting. GitLab issue #671.
  Thanks to Lennart Sauerbeck (@lennart_s) for the report.
- Add makefile target to launch a production staging Docker image.
- Improve duplicated document list view logic to not show
  documents with trashed duplicates.
- Backport Docker composer makefile targets.
- Add PermissionTestCaseMixin and SmartSettingTestCaseMixin to better
  organize cache invalidation of both apps for tests.
- Add a version attribute to setting namespace. These are dumped
  as SMART_SETTINGS_NAMESPACES.
- Add savesettings command.
- Add extra logging to the IMAP email source. GitLab issue #682.
  Thanks to Patrick Hütter (@PatrickHuetter) for the report.
- Rename all instances of the IMAP server from mailbox to
  server for clarity.
- Add book link in the about menu.
- Add unknown exception handling when checking for the latest
  version.

3.2.8 (2019-10-01)
==================
- Fix error when accessing some API entry points without
  being authenticated.
- Add cabinet add and remove workflow actions.
- Tweaked the jstree component's appearance to cope with
  long cabinet labels.
- Update Django to version 1.11.24
- Update jQuery to version 3.4.1
- Add support for deleting the OCR content of a document
  or selection of documents.
- Add OCR content deleted event.
- Add missing recursive option to Docker entrypoint
  chown. GitLab issue #668. Thanks to John Wice (@brilthor)
  for the report.
- Add support for deleting the parsed content of a document
  of selection of documents.
- Add parsed content deleted event.
- Allow scaling of UI on mobile devices.
- Add Chinese fonts to the Docker image

3.2.7 (2019-08-28)
==================
- Fix checkout form bug. Thanks to Lucius Schaerer
  (@lschaer1) for the report.
- Disable pagination current page button
  Current page button was clickable and would cause the
  single page navigation to jump to the home view.
- Remove redundant Celery queue declarations from the
  file_metadata app.
- Add internal_name field to workflow serializer.
  Fixes workflow API creation view.
- Fix document cabinet list API view. Thanks for forum user
  "jere" for the report. Forum topic 1039.
- Fix document template column field. GitLab issue #655.
  Thanks to Christian Wiegand (@christianwgd) for the
  report.
- Increase mailing profile password field max length
  from 48 to 128 characters. GitLab issue #657.
  Thanks to sigsec (@sigsec) for the report.
- Update the Docker entrypoint to update the ownership
  of files when the UID of GUID are changed.
  GitLab issue #650. Thanks to Fabian (@ruffy91)
  for the report.
- Update the Docker entrypoint to allow changing
  the GID of the mayan user to existing values.
  GitLab issue #652. Thanks to Fabian (@ruffy91)
  for the report.
- Rename the MAYAN_USER_GUID environment variable
  to MAYAN_USER_GID.
- Add automatic adjustment of HTML body on navigation
  bar changes. Closes GitLab issue #643. Thanks to
  Light Templar (@LightTemplar) for the report.
- Unify all line endings to be Linux style.
- Make sure system alerts don't appear under
  floating elements.

3.2.6 (2019-07-10)
==================
- Remove the smart settings app * import.
- Encode settings YAML before hashing.
- Fix document icon used in the workflow runtime links.
- Add trashed date time label.
- Fix thumbnail generation issue. GitLab issue #637.
  Thanks to Giacomo Cariello (@giacomocariello) for the report
  and the merge request fixing the issue.

3.2.5 (2019-07-05)
==================
- Don't error out if the EXTRA_APPS or the DISABLED_APPS settings
  are set to blank.
- Update troubleshooting documentation topic.
- Add data migration to the file metadata app. Synchronizes the
  document type settings model of existing document types.
- Fix cabinet and tags upload wizard steps missing some entries.
  GitLab issue #632. Thanks to Matthias Urhahn (@d4rken) for the
  report.
- Add alert when settings are changed and util the installation
  is restarted. GitLab issue #605. Thanks to
  Vikas Kedia (@vikaskedia) to the report.
- Update Django to version 1.11.22, PyYAML to version 5.1.1,
  django-widget-tweaks to version 1.4.5, pathlib2 to version 2.3.4,
  Werkzeug to version 0.15.4, django-extensions to version 2.1.9,
  django-rosetta to version 0.9.3, psutil to version 5.6.3.

3.2.4 (2019-06-29)
==================
- Support configurable GUnicorn timeouts. Defaults to
  current value of 120 seconds.
- Fix help text of the platformtemplate command.
- Fix IMAP4 mailbox.store flags argument. Python's documentation
  incorrectly state it is named flag_list. Closes GitLab issue
  #606.
- Improve the workflow preview generation. Use polylines
  instead of splines. Add state actions to the preview.
  Highlight the initial state.
- Add help text to the workflow transition form comment field.
- Fix direct deployment instructions.
- Add user, group, and role dashboard widgets.
- Add test mixin detect database connection leaks.
- Remove tag create event registration from the tag
  instances. The tag create event is not applicable to
  existing tags.
- Add proper redirection after moving a document to the
  trash.
- Remove the INSTALLED_APPS setting. Replace it with
  the new COMMON_EXTRA_APPS and COMMON_DISABLED_APPS.
- Improve email metadata support. Can now work on
  email with nested parts. Also the metadata.yaml
  attachment no longer needs to be the first attachment.

3.2.3 (2019-06-21)
==================
- Add support for disabling the random primary key
  test mixin.
- Fix mailing profile log columns mappings.
  GitLab issue #626. Thanks to Jesaja Everling (@jeverling)
  for the report.
- Fix the Django SMTP backend username field name.
  GitLab issue #625. Thanks to Jesaja Everling (@jeverling)
  for the report and the research.
- Increase the Django STMP username.
  GitLab issue #625. Thanks to Jesaja Everling (@jeverling)
  for the report and the research.

3.2.2 (2019-06-19)
==================
- Fix document type change view. Closes GitLab issue #614
  Thanks to Christoph Roeder (@brightdroid) for the report.
- Fix document parsing tool view typo. Closes GitLab issue #615.
  Thanks to Tyler Page (@iamtpage) for the report.
- Update the task_check_interval_source reference
  GitLab issue #617. Thanks to Lukas Gill (@lukkigi) for
  the report and debug information.

3.2.1 (2019-06-14)
==================
- Fix sub cabinet creation view. Thanks to Frédéric Sheedy
  (@fsheedy) for the report.
- Add PostgreSQL troubleshooting entry. Closes GitLab
  issues #523 and #602
- Use YAML SafeDumper to avoid adding YAML datatype tags.
  Closes GitLab issue #599. Thanks to Frédéric Sheedy
  (@fsheedy) for the report and debug information.
- Add check for app references and point users to release notes for details.
  GitLab issue #603. Thanks to Vikas Kedia (@vikaskedia) for the report.
- Remove sidebar floar right.
  Fixed GitLab issue #600. Thanks to Frédéric Sheedy
  (@fsheedy) for the report and debug information.
- Collapse sidebar on small screen
  Display sidebar at the bottom of the screen on small displays.

3.2 (2019-06-13)
================
- Split sources models into separate modules.
- Add support for subfolder scanning to watchfolders. Closes
  GitLab issue #498 and #563.
- Updated the source check behavior to allow checking a source
  even when the source is disabled and to not deleted processed files
  during a check.
- Switch to full app paths.
- Split document app models into separate modules.
- Split workflow views into separate modules.
- Add custom DatabaseWarning to tag the SQLite usage warning.
- Add keyword arguments to add_to_class instances.
- Move add_to_class function to their own module called methods.py
- Remove catch all exception handling for the check in and
  check out views.
- Improve checkouts tests code reducing redundant code.
- Change how the HOME_VIEW setting is defined.
- Remove the role permission grant and revoke permission.
- Split trashed document views into their own module.
- Show entire sys trace when an App import exception is raised.
- Remove Django suit from requirements.
- Remove development URLs from main URL file.
- Move API documentation generation from the root URLs module
  to the REST API app's URLs module.
- Update Pillow to version 6.0.0
- Update PyYAML to version 5.1. Update use of safe_load and
  safe_dump to load and dump using the SafeLoader.
- Add SilenceLoggerTestCaseMixin to lower level of loggers
  during tests.
- New default value for setting DOCUMENTS_HASH_BLOCK_SIZE is
  65535.
- New default value for setting MIMETYPE_FILE_READ_SIZE is
  1024.
- Add workaround for Tesseract bug 1670
  https://github.com/tesseract-ocr/tesseract/issues/1670
  https://github.com/tesseract-ocr/tesseract/commit/3292484f67af8bdda23aa5e510918d0115785291
  https://gitlab.gnome.org/World/OpenPaperwork/pyocr/issues/104
- Move setting COMMON_TEMPORARY_DIRECTORY to the storage app.
  The setting is now STORAGE_TEMPORARY_DIRECTORY.
- Move file related utilities to the storage app.
- Backport and remove unused code from the permission app.
- Move the navigation and authentication templates to their
  respective apps.
- Add dashboard app.
- Remove queryset slicing hack from the Document list view.
  And slice the Recently Added Document queryset itself.
- Move stub filtering to the Document model manager.
- Increase the default number of recently added documents and
  recently accessed documents from 40 to 400.
- Integrate django-autoadmin into the core apps.
- Update middleware to new style classes.
- Add server side invalid document template.
- Move tag specific JavaScript to the tags app.
- Reduce form boilerplate code with new FormOptions class.
- Use FormOptions for the DetailForm class.
- DetailForm now support help text on extra fields.
- Add FilteredSelectionForm class.
- Use FilteredSelectionForm for TagMultipleSelectionForm.
- Use FilteredSelectionForm for the class CabinetListForm.
- Add keyword arguments to URL definitions.
- Use FilteredSelectionForm to add a new ACLCreateForm.
- Rename IndexListForm to IndexTemplateFilteredForm.
- Use FilteredSelectionForm for IndexTemplateFilteredForm.
- Use FilteredSelectionForm for DocumentVersionSignatureCreateForm.
- Improve document signatures tests.
- Add docstrings to most models.
- Add support to the mailing profiles for specifying a from
  address. Closes GitLab issue #522.
- Expose new Django settings: AUTH_PASSWORD_VALIDATORS, DEFAULT_FROM_EMAIL,
  EMAIL_TIMEOUT, INTERNAL_IPS, LANGUAGES, LANGUAGE_CODE, STATIC_URL,
  STATICFILES_STORAGE, TIME_ZONE, WSGI_APPLICATION.
- Convert language choices into a function.
- Move language choices generation to documents.utils.
- Remove support for generating documents images in base 64
  format.
- Move Pillow initialization from the module to the backend
  class initialization.
- Remove star import from the ACL and Common apps.
- Add dependencies app
- Convert the document tags widget to use HTML templates.
- Move Tag app HTML widgets to their own module.
- Move the document index app widgets to the html_widget.py
  module.
- Update group members view permission. The group edit and
  user edit permission are now required.
- Add keyword arguments to messages uses.
- Add keyword arguments to the reverse use in views.
- Add MERCs 5 and 6.
- Update authentication function views to use Django's new class
  based authentication views.
- Expose Django's LOGOUT_REDIRECT_URL setting.
- Move current user views from the common app to the user
  management app.
- Move the purge permission logic to the StorePermission
  manager.
- Remove the MIMETYPE_FILE_READ_SIZE setting.
- Use copyfileobj in the document parsers.
- Backport list facet menu code.
- Backport sidebar code.
- CSS updates to maximize usable width.
- Improve partial navigation error messages and display.
- Add user created and user edited events.
- Add group created and group edited events.
- Add support for SourceColumn widgets.
- Improve styling of the template debug view.
- Add support for showing the current user's events.
- Add support kwargs to the SourceColumn class.
- Improve the event widgets, views and tests.
- Add mailer use event.
- Remove the include fontawesome and download it from
  the NPMregistry.
- Fix issue installing scoped NPM packages.
- Add new icons classes and templates.
- Add support for icon composition.
- Add support for link icon path imports.
- Remove support for link icon strings.
- Split document app form into separate modules.
- Move the favorite document views to their own module.
- Replace DocumentTypeSelectioForm with an improved
  version that does filtering.
- Update OCR links activation.
- Update document parsing link activation.
- Add favorite document views tests.
- Add document state action view test.
- Remove sidebar menu instance. The secondary menu and the
  previour sidebar menu now perform the same function.
- Backport source column identifiable and sortable
  improvements.
- Update the way the no-result template is shown.
- Improve TwoStateWidget to use a template. Make
  it compatible with the SourceColumn.
- Update SourceColumn to support related attributes.
- Add support for display for empty values for
  source columns.
- Add support for source column object or attribute
  absolute URLs.
- Add sortable columns to all apps.
- Remove permission list display from the ACL list view.
  Reduces clutter and unpredictable column size.
- Remove the full name from the user list.
- Add the first name and last name to the user list.
- Add file metadata app.
- Add support for submitting forms by pressing the
  Enter key or by double clicking.
- Rename form template 'form_class' to 'form_css_classes'.
- Add support for adding form button aside from the
  default submit and cancel.
- Update ChoiceForm to be full height.
- Add AddRemoveView to replace AssignRemoveView
- Update the group roles view to use the new AddRemoveView.
- Add role create and edit events.
- Sort users by lastname, firstname.
- Switch user groups and group users views to AddRemoveView.
- Commit user edit event when an user is added or removed
  from a group.
- Commit the group edit event when a group is added or remove
  from an user.
- Require dual permissions when add or removing users to and
  from group. Same with group to users.
- Backport search improvements.
- Remove search elapsed time calculation.
- Remove SEARCH_LIMIT setting.
- Use the 'handler' prefix for all the signal handler functions.
- Remove custom email widget and use Django's.
- Increase default maximum number of favorite documents to 400.
- Update the role group list view to use the new AddRemoveView.
- Commit the group event in conjunction with the role event
  when a group is added or remove from role.
- Update the role permission view to use the new AddRemoveView.
- Rename transformation manager method add_for_model to
  add_to_object.
- Rename transformation manager method get_for_model to
  get_for_object.
- Load the converter class on demand.
- Remove app top level star imports.
- Monkeypatch group and user models to make their fields
  translatable.
- Add new and default Tesseract OCR backend to avoid
  Tesseract bug 1670
  (https://github.com/tesseract-ocr/tesseract/issues/1670)
- Load only one language in the document properties form.
- Convert title calculation form to a template tag.
- Show the full title as a hover title even when truncated.
- Increase default title truncation length to 120 characters.
- Improve inherited permission computation.
- Add test case mixin that produces ephimeral models.
- Update ACL permissions view to use the new AddRemoveView class.
- Add ACL created and edited events.
- Update index document types view to use the new AddRemoveView
  class.
- Add index create and edit events.
- Allow overloading the action_add and action_remove methods
  from the AddRemoveView.
- Add view to link document type and indexes from the document
  type side.
- Update smart link document type selection view to use
  AddRemoveView class.
- Add smart link created and edited events.
- Fix smart link ACL support.
- Update JavaScript downloader to work with Python 3.
- Improve speed of the NPM package hash verification.
- Add view to enable smart links for documents types
  from the document type side.
- Enable list link icons.
- Add outline links CSS for facets.
- Add a bottom margin to list links.
- Use copyfileobj to save documents to files
- Add user logged in and logged out events.
- Add transaction handling in more places.
- Update ACLs tests to use ephimeral models.
- Add new app to handle all dependencies.
- Remove the licenses.py module and replace
  it with a dependencies.py module.
- Backport ACL computation improvements.
- Remove model permission proxy models.
- Remove related access control argument. This is
  now handled by the related field registration.
- Allow nested access control checking.
- check_access's permissions argument must now be
  an interable.
- Remove permissions_related from links.
- Remove mayan_permission_attribute_check from
  API permission.
- Update Bootstrap and Bootswatch to version 3.4.1.
- Convert the workflow document types view to use
  the new AddRemove view.
- Add the workflow created and edited events.
- Remove AssignRemove View.
- Add view to setup workflows per document type
  from the document type side.
- Make workflows, workflows states, workflow
  transitions column sortable.
- Show completion and intial state in the
  workflow proxy instance menu list.
- Fix translation of the source upload forms
  using dropzone.js
- Rename get_object_list to get_source_queryset.
- Add uniqueness validation to SingleObjectCreateView.
- Remove MultipleInstanceActionMixin.
- Backport MultipleObjectMixin improvements.
- Remove ObjectListPermissionFilterMixin.
- Add deprecation warning to convertdb
- Add the preparestatic command.
- Remove the related attribute of check_access.
- Remove filter_by_access. Replaced by restrict_queryset.
- Move the user set password views to the authentication app.
- All views redirect to common's home view instead of the
  REDIRECT_URL setting.
- Update tag document list and the document tag list
  views to require the view permissions for both objects.
- Install and server static content to and from the image.
- Add support for editing document comments.
- Remove Internet Explorer specific markup.
- Fix optional metadata remove when mixed with required
  metadata.
- Create intermedia file cache folder. Fixes preview errors
  when the first document uploaded is an office file.
- Move queue and task registration to the CeleryQueue class.
  The .queues.py module is now loaded automatically.
- Allow setting the Docker user UID and GUID.
- Add task path validation.
- Increase dropzone upload file size limit to 2GB.
- Add cabinet created and edited events.
- Show a null mailer backend if there is backend with an
  invalid path. Due to the app full path change, existing
  mailer setups need to be recreated.
- The document link URL when mailed is now composed of the
  COMMON_PROJECT_URL + document URL instead of the Site
  domain.
- Add the checkdependencies command.
- Add comment and make file target to generate all requirement
  files.
- Place deletion policies units before periods for clarity.
- Remove repeated EMAIL_TIMEOUT setting.
- Invert order to the Action Object and Target columns for
  clarity.
- Add note about the new preparestatic command.
- Add no-result template for workflow instance detail view.
- Update HTTP workflow action to new requests API.
- Remove the included Lato font. The font is now downloaded
  at install time.
- Add support for Google Fonts dependencies.
- Add support for patchin dependency files using rewriting rules.
- Allow searching documents by UUID.
- Improve search negation logic.
- Add support for search field transformations.
- Disable hiding page navigation on idle.
- Display namespace in the transition trigger view.
- Sort events list in the transition trigger view.
- Add support for form media to DynamicFormMixin.
- Fix tag attach and remove action form media.
- Sort content type list of the access grant and remove action.
- Use select2 for the content type filed of the access
  grant and remove action.
- Add Latvian translation.
- Support search model selection.
- Support passing a queryset factory to the search model.
- Add workflow actions to grant or remove permissions to
  a document.
- Add support for locked files for watchfolder.

3.1.11 (2019-04-XX)
===================
- Fix multiple tag selection wizard step.
- Change the required permission for the checkout info link from
  document check in to document checkout details view.
- Lower the log severity when links don't resolve.
- Add DOCUMENTS_HASH_BLOCK_SIZE to control the size of the file
  block when calculating a document's checksum.

3.1.10 (2019-04-04)
===================
- Backport test case improvements from the development branch. Add random
  primary key mixin. Split test case code into mixins. Make the view test
  case and the API test cases part of the same class hierarchy. Update tests
  that failed due to the new import locations.
- Add support for disabling the content type checking test case mixin.
- Update document indexing tests to be order agnostic. GitLab issue #559.
- Add test for the advanced search API.
- Apply merge !36 by Simeon Walker (@simeon-walker) to fix the advanced
  search API.
- Apply merge !35 by Manoel Brunnen (@mbru) to fix building the Docker image
  on the armv7l platform (RasperryPi, Odroid XU4, Odroid HC2). Also fixes
  assertion errors from pip (https://github.com/pypa/pip/issues/6197).
- Apply merge !37 by Roger Hunwicks (@roger.hunwicks) to allow
  TestViewTestCaseMixin to work with a custom ROOT_URLCONF. GitLab issue
  #566.
- Apply merge !40 by Roger Hunwicks (@/roger.hunwicks) to pin the Tornado
  version used to 6.0 and continue supporting Python 2.7. GitLab issue #568.
- Apply merge !41 by Jorge E. Gomez (@jorgeegomez) to fix the compressed
  class method name. GitLab issue #572.
- Remove notification badge AJAX setup. Individual link AJAX workers are
  obsolete now that the menu is being rendered by its own AJAX renderer.
  GitLab issue #562.
- Add support for server side link badges.
- Add API to list all templates.
- Remove newlines from the rendered templates.
- Reject emails attachments of size 0. Thanks to Robert Schoeftner
  (@robert.schoeftner)for the report and solution. GitLab issue #574.
- Add missing document index API view create permission.
- Fix index list API view. Add index create, delete, detail API tests.
  GitLab issue #564. Thanks to the Stéphane (@shoyu) for the report and
  debug information.
- Validate the state completion value before saving. Thanks to
  Manoel Brunnen (@mbru) for the report and debug information.
  GitLab issue #557.
- Add the MIMETYPE_FILE_READ_SIZE setting to limit the number of bytes read
  to determine the MIME type of a new document.
- Force object to text when raising PermissionDenied to avoid
  UnicodeDecodeError. Thanks to Mathias Behrle (@mbehrle) for the report
  and the debug information. GitLab issue #576.
- Add support for skipping a default set of tests.

3.1.9 (2018-11-01)
==================
- Convert the furl instance to text to allow serializing it into
  JSON to be passed as arguments to the background task.

3.1.8 (2018-10-31)
==================
- Reorganize documentation into topics and chapters.
- Add Workflows and API chapters.
- Add new material from the Wiki to the documentation.
- Add data migrations to the sources app migraton 0019 to ensure all labels
  are unique before performing the schema migations.
- Add improvements to the metadata URL encoding and decoding to support
  ampersand characters as part of the metadata value. GitLab issue
  #529. Thanks to Mark Maglana @relaxdiego for the report.
- Add custom validator for multiple emails in a single text field.
  Change the widget of the email fields in the mailer app to avoid
  browser side email validation. Closes GitLab issue #530.
  Thanks to Mark Maglana @relaxdiego for the report.
- Add configuration option to change the project/installation URL.
  This is used in the password reset emails and in the default
  document mailing templates.
- Increase the size of the workflow preview image.
- Center the workflow preview image.
- Move the noop OCR backend to the right place.
- Add new management command to display the current configuration
  settings.
- Default the YAML flow format to False which never uses inline.
- Add support for reindexing documents when their base properties like
  the label and description are edited.

3.1.7 (2018-10-14)
==================
- Fix an issue with some browsers not firing the .load event on cached
  images. Ref: http://api.jquery.com/load-event/
- Remove duplicate YAML loading of environment variables.
- Don't load development apps if they are already loaded.
- Make sure all key used as input for the cache key hash are
  bytes and not unicode. GitLab issue #520. Thanks to TheOneValen
  @TheOneValen for the report.
- Ignore document stub from the index mirror. GitLab issue
  #520. Thanks to TheOneValen @TheOneValen for the report.
- Fix for the Docker image INSTALL_FLAG path. Thanks to
  Mark Maglana @relaxdiego for the report and to Hamish Farroq @farroq_HAM
  for the patch. GitLab issue #525.
- Fix the typo in the Docker variable for worker concurrency. Thanks to
  Mark Maglana @relaxdiego for the report and to Hamish Farroq @farroq_HAM
  for the patch. GitLab issue #527.
- Add a noop OCR backend that disables OCR and the check for the
  Tesseract OCR binaries. Set the OCR_BACKEND setting or MAYAN_OCR_BACKEND
  environment variable to ocr.backends.pyocr.PyOCR to use this.
- All tests pass on Python 3.
- documentation: Add Docker installation method using a dedicated
  Docker network.
- documentation: Add scaling up chapter.
- documentation: Add S3 storage configuration section.

3.1.6 (2018-10-09)
==================
- Improve index mirroring value clean up code to remove the spaces at the
  starts and at the end of directories. Closes again GitLab issue #520
  Thanks to TheOneValen @ for the report.
- Improve index mirroring cache class to use the hash of the keys
  instead of the literal keys. Avoid warning about invalid key
  characters. Closes GitLab issue #518. Thanks to TheOneValen @ for the
  report.
- Only render the Template API view for authenticated users.
  Thanks rgarcia for the report.
- Add icon to the cabinet "Add new level" link.
- Display the cabinet "Add new level" link in the top level view too.

3.1.5 (2018-10-08)
==================
- Consolidate some document indexing test code into a new mixin.
- Split the code of the mountindex command to be able to add tests.
- Fix the way the children of IndexInstanceNode are accessed. Fixes GitLab
  issue #518. Thanks to TheOneValen @TheOneValen for the report.
- Remove newlines from the index name levels before using them as FUSE
  directories.
- Fixed duplicated FUSE directory removal.
- Add link and view to show the parsed content of each document page.
- Add a modelform for adding and editing transformation and perform YAML
  validation of arguments.
- Add stricted error checking to the crop transformation.
- Update compressed files class module to work with Python 3.
- Update document parsing app tests to work with Python 3.
- Handle office files in explicit binary mode for Python 3.
- Return a proper list of SearchModel instances (Python 3).
- Specify FUSE literals in explicit octal notation (Python 3).
- URL quote the encoded names of the staging files using Django's compat
  module. (Python 3)
- Open staging file in explicit binary mode. (Python 3)
- Add separate Python 2 and Python 3 versions of the MetadataType model
  .comma_splitter() static method.
- Update the metadata app tests to work on Python 3.
- Make sure metadata lookup choices are a list to be able to add the
  optional marker (Python 3).
- Make sure the image in the document preview view is centered when it is
  smaller than the viewport.
- Restore use of the .store_body variable accidentally remove in
  63a77d0235ffef3cd49924ba280879313c622682. Closes GitLab issue #519.
  Thanks to TheOneValen @TheOneValen for the report.
- Add shared cache class and add mounted index cache invalidation when
  document and index instance nodes are updated or deleted.
- Fix document metadata app view error when adding multiple optional
  metadata types. Closes GitLab issue #521. Thanks to the TheOneValen
  @TheOneValen for the report.

3.1.4 (2018-10-04)
==================
- Fix the link to the documenation. Closes GitLab issue #516.
  Thanks to Matthias Urlichs @smurfix for the report.
- Update related links. Add links to the new Wiki and Forum.
- Add Redis config entries in the Docker images to disable
  saving the database and to only provision 1 database.
- Remove use of hard coded font icon for document page
  rendering busy indicator.
- Disable the fancybox caption link if the document is
  in the trash.
- Load the DropZone CSS from package and remove the
  hard code CSS from appearance/base.css.
- Add support for indexing on OCR content changes.
- Add support for reindexing document on content parsing
  changes.
- Strip HTML entities from the browser's window title.
  Closes GitLab issue #517. Thanks to Daniel Carrico @daniel1113
  for the report.
- Improve search app. Refactored to resolve search queries
  by terms first then by field.
- Add explanation to the launch workflows tool.

3.1.3 (2018-09-27)
==================
- Make sure template API renders in non US languages.
- Fix user groups view.
- Add no results help text to the document type -> metadata type
  association view.
- Expose the Django INSTALLED_APPS setting.
- Add support for changing the concurrency of the Celery workers in the
  Docker image. Add environment variables MAYAN_WORKER_FAST_CONCURRENCY,
  MAYAN_WORKER_MEDIUM_CONCURRENCY and MAYAN_WORKER_SLOW_CONCURRENCY.
- Add latest translation updates.
- Fixes a few text typos.
- Documentation updates in the deployment and docker chapters.

3.1.2 (2018-09-21)
==================
- Database access in data migrations defaults to the 'default' database.
  Force it to the user selected database instead.
- Don't use a hardcoded database alias for the destination of the database
  conversion.
- Improve natural key support in the UserOptions model.
- Update from Django 1.11.11 to 1.11.15.
- Add support to the convertdb command to operate on specified apps too.
- Add test mixin to test the db conversion (dumping and loading) of a
  specific app.
- Add an user test mixin to group user testing.
- Add test the user managament app for database conversion.
- Add support for natural keys to the DocumentPageImageCache model.
- Add database conversion test to the common app.
- Fix label display for resolved smart links when not using a dynamic label.
- Only show smart link resolution errors to the user with the smart link
  edit permission.
- Intercept document list view exception and display them as an error
  message.

3.1.1 (2018-09-18)
==================
- CSS tweak to make sure the AJAX spinner stays in place.
- Fix 90, 180 and 270 degrees rotation transformations.

3.1 (2018-09-17)
================
- Improve database vendor migration support
- Add convertdb management command.
- Add error checking to the crop transformation arguments.
- Update dropzone.js' timeout from 30 seconds to 120 to allow upload
  of large files on slow connections.
- Increase gunicorn's timeout from 30 seconds to 120.
- Update packages versions: Pillow:5.2.0, PyYAML:3.13, django-environ:0.4.5,
  django-model-utils:3.1.2, django-mptt:0.9.1, django-widget-tweaks: 1.4.2,
  flanker:0.9.0, flex:6.13.2, furl:1.2, gevent:1.3.5, graphviz: 0.8.4,
  gunicorn:19.9.0, pyocr:0.5.2, python-dateutil:2.7.3
- Remove use of django-compressor and cssmin now that the project used
  Whitenoise.
- Display error when attempting to recalculate the page count of an empty
  document (document stub that has no document version).
- Add support for client side caching of document page images. The time
  the images are cached is controlled by the new setting
  DOCUMENTS_PAGE_IMAGE_CACHE_TIME which defaults to 31556926 seconds
  (1 year).
- The document quick label selection field now uses a select2 widget.
- Include querystring when force reload of a bare template view.
- Speed up document image fade in reveal.
- Use reseteable timer to ensure more document panels heights are matched.
- Rewrote Mayan's JavaScript suite MayanApp into ECMAScript2015.
- Remove use is waitForJQuery.
- Remove code statistics from the documentation.
- Remove the pending work chapter. This is now available in the Wiki:
  wiki.mayan-edms.com
- Unify template title rendering.
- Add support for template subtitles.
- Make sure the on entry action of the initial state of workflows
  executes on document creation.
- Add new document app events: document type created and document type
  edited.
- Add link to document type events.
- Add new metadata app events: metadata type created, metadata type edited,
  metadata type to document type relationship update.
- Add link to metadata type events.
- Add support for subscribing to metadata type events.
- Add link to view the events of a tag.
- Add support for subscribing to the events of a tag.
- Add the tag events view permissions to the tag model ACL.
- Hide the title link of documents in the trash.
- Add support for document metadata events: add, edit and remove.
- Add workflow action to update the label and description of a document.
- Add COMMON_PROJECT_TITLE as a setting option to customize the title
  string.
- Add support for YAML configuration files.
- Add support for editing setting options and saving them using the
  new YAML configuration file support.
- Add new revertsettings management command.
- Add new permission to edit setting via the UI.
- Renamed setting LOCK_MANAGER_DEFAULT_BACKEND to LOCK_MANAGER_BACKEND.
- Add help texts to more setting options.
- Add ACL support for metadata types.
- Add cascade permission checks for links. Avoid allowing users
  to reach a empty views because they don't access to any of
  the view's objects.
- Apply link permission cascade checks to the message of the day,
  indexing and parsing, setup link.
- Add ACL support to the message of the day app.
- The index rebuild permission can now be set as part of the index
  ACL for each individual index.
- Add cascade permission check to the index rebuild tool link.
- The index rebuild tool now responds with the number of indexes
  queued to rebuild instead of a static acknowledment.
- Add missing permission check to the document duplicate scan
  link.
- Add new document indexing permission. This permission allows
  user to view an index instance as opposed to the current
  permission which allows viewing an index definiton on the
  setup menu.
- Add support to conditionally disable menus.
- Disable the Tags menu when the user doesn't have the
  tag create permission or the tag view access for any tag.
- Disable the Cabinets menu when the user doesn't have the
  cabinet create permission or the cabinet view permission
  for any cabinet.
- Update forum link in the about menu.
- Only show the settings namespace list link where it is
  relevant.
- Add support for the fillcolor argument to the rotate
  transformation.
- Sort documents by label.
- Add recently added document list view. The setting
  DOCUMENTS_RECENT_COUNT has been renamed to
  DOCUMENTS_RECENT_ACCESS_COUNT. New setting
  DOCUMENTS_RECENT_ADDED_COUNT added.
- Use platform independant hashing for transformations.
- Add support to the ObjectActionMixin to report on instance action
  failures. Add also an error_message class property and the new
  ActionError exception.
- Add favorite documents per user. Adds new setting option
  DOCUMENTS_FAVORITE_COUNT.
- Add new class based dashboard widget. This new widget supports
  subclassing and is template based. All exising widgets have been
  converted. ACL filtering was added to the widget results.
- In addition to the document view permission, the checkout detail
  view permission is now needed to view the list of checked out
  document.
- After queuing a chart for update, the view will now redirect
  to the same chart.
- The multiple document action dropdown is now sorted alphabetically.
- Improve statistics subclassing. Split class module into classes
  and renderers.
- Sort facet link, object, secondady and sidebar actions.
- Add support for extended templates when there are no results.
- Add help messages and useful links to several apps when there
  are no results available.
- Add a new column to settings showing if they are overrided
  via environment variable.
- The official config filename is config.yml.
- Interpret ALLOWED_HOSTS as YAML.
- Don't show the document types of an index instance.
- Add the tag created and tag edited events.
- Add support for blocking the changing of password for specify users.
- Add support for changing the HOME_VIEW, LOGIN_URL and LOGIN_REDIRECT_URL
  from the settings view.
- Instead of the document content view, the document type parsing setup
  permissions is now required to view the parsing error list.
- The document type parsing setup permission can now be granted for
  individual document types.
- Add link to view a specific page's OCR content.
- Remove the duplicated setting pdftotext_path from the OCR path.
  This is now handled by the document parsing app.
- Implement partial refresh of the main menu.
- Remove usage of pace.js. Would cause XMLRequest to fallback to
  synchronous mode.
- Add custom AJAX spinner.
- Complete refactor of the compress archive class support. Closes
  GitLab issue #7.
- Add support for preserving the extension of document files when
  using the quick label feature. Added to the document properties
  edit view and the document upload view. Closes GitLab issue
  #360.
- Add new dashboard item to display the total page count.
- Show the document type being uploaded in the source view title.
- Setting SOURCE_SCANIMAGE_PATH is now SOURCES_SCANIMAGE_PATH.
- Refactor the staging file image generation to support
  background task generation, caching and cache sharing.
- New queue: sources_fast. Used for staging file generation.
- New settings: SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND and
  SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS to control
  where and how staging file caching is done.
- Fix an edge case on the document indexing where an empty
  node could be left behind.
- Improve the speed of the document indexing.
- Move the matchHeight call from lazy loading to image loading.
  Reduces the chance of wrongly sized cards.
- Generalize the JavaScript menu rendering into an API for
  templates that only refresh the menu when there are changes.
  Closes GitLab issue #511. Thanks to Daniel Carrico
  @daniel1113 for the report.
- Refactor the ModelAttribute class into two separate classes:
  ModelAttribute for executable model attributes and ModelField
  for actual ORM fields.
- Expose more document fields for use in smart links.
- The size of the document type label field has been increased
  from 32 to 96 characters.
- Add file_size and datetime fields to the DocumentPageCachedImage
  model.
- Make icon classes file template based.
- Add the current step and total steps of a wizard in the template context.
- Chart updates: Show last update date and time in list view and details
  view. Change color scheme to match rest of project. Increase size of
  data points. Improve responsive settings. Redirect to the current view
  after queueing.
- Split document type retention policies into it own view.

3.0.3 (2018-08-17)
==================
- Tags app: Add explicit casting of escaped tag labels to prevent exploit
  of cross site scripting. Thanks to Lokesh (@lokesh1095) for
  the report and proposed solutions. Closes GitLab issue #496.
- Tags app: Add explicit post action redirect for the tag attach and
  tag remove actions when working on a single document.

3.0.2 (2018-08-16)
==================
- Docker install script: Default to verbose.
- Docker install script: Increase startup timer to 10 seconds.
- Docker install script: Allow configuring the PostgreSQL port.
- Documentation: Add deployment step that configures Redis to discard
  unused task data when it runs out of memory.
- Index app: Add natural key support to the Index model.
- Mailer app: Add natural key support to the mailer app.
- Cabinets: Redirect to the cabinet list view after creating a new cabinet.
- Builds: Limit the number of branches that trigger the full test suit.
- Converter app: Fix crop transformation argument parsing.
- Converter app: Add error checking to the crop transformation arguments.
  Thanks to Jordan Wages (@wagesj45) for the report and investigation on
  the issue. Closes GitLab issue #490
- Common app: Fix post login redirection to honor the ?next= URL query
  string argument. Thanks go to K.C. Wong (@dvusboy1). Closes GitLab
  issue #489.
- Docker install script: Detect if Docker installed and provide help
  text if not.
- Sources app: Update dropzone.js' timeout from 30 seconds to 120 to allow
  upload of large files on slow connections.
- Documentation: Increase gunicorn's timeout from 30 seconds to 120.
- Documents app: Display error when attempting to recalculate the page
  count of an empty
  document (document stub that has no document version).
- Appearance app: Include querystring when force reload of a bare template
  view.
- Documents app: Fix trashed document count and document page count swapped
  dashboard icons.
- Documents app: Rename the multi document download link from "Download" to
  "Advanced download" for consistency.
- Documentation: Remove code statistics from the documentation.
- Documentation: Remove the pending work chapter. This is now available in
  the Wiki: wiki.mayan-edms.com
- Appearance app: Add support for hiding a links icon. Hide all object menu
  links' icons.
- Documents app: Hide the title link of documents in the trash.
- Workflow app: Define a redirection after workflow actions are edited.
- Appearance app: avoid setting window.location directly to avoid exploit
  of cross site scripting. Thanks to Lokesh (@lokesh1095) for the report
  and solution. Closes GitLab issue #494.
- Cabinets app: Escape cabinet labels to avoid possible exploit of
  cross site scripting. Thanks to Lokesh (@lokesh1095) for the report
  and proposed solutions. Closes GitLab issue #495.
- Language translation synchonization.

3.0.1 (2018-07-08)
==================
- Pin javascript libraries to specific versions to avoid using
  potentianlly broken updates automatically. GitLab issue #486.
- French and Polish language translation updates.
- Merge request #25. Thanks to Daniel Albert @esclear
  for the patch.

3.0 (2018-06-29)
================
- Rename the role groups link label from "Members" to "Groups".
- Rename the group users link label from "Members" to "Users".
- Don't show full document version label in the heading of the document
  version list view.
- Show the number of pages of a document and of document versions in
  the document list view and document versions list views respectively.
- Display a document version's thumbnail before other attributes.
- User Django's provided form for setting an users password.
  This change allows displaying the current password policies
  and validation.
- Add method to modify a group's role membership from the group's
  view.
- Rename the group user count column label from "Members" to "Users".
- Backport support for global and object event notification.
  GitLab issue #262.
- Remove Vagrant section of the document. Anything related to
  Vagrant has been move into its own repository at:
  https://gitlab.com/mayan-edms/mayan-edms-vagrant
- Add view to show list of events performed by an user.
- Allow filtering an event list by clicking on the user column.
- Display a proper message in the document type metadata type relationship
  view when there are no metadata types exist.
- Require the document view permission to view trashed documents.
- Make the multi object form perform an auto submit when the value is
  changed.
- Improved styling and interaction of the multiple object action form.
- Add checkbox to allow selecting all item in the item list view.
- Revise and improve permission requirements for the documents app API.
- Downloading a document version now requires the document download
  permission instead of just the document view permission.
- Creating a new document no longer works by having the document create
  permission in a global manner. It is now possible to create a document via
  the API by having the document permission for a specific document type.
- Viewing the version list of a document now required the document version
  view permission instead of the document view permission.
- Not having the document version view permission for a document will not
  return a 403 error. Instead a blank response will be returned.
- Reverting a document via API will new require the document version revert
  permission instead of the document edit permission.
- Fix permission filtering when performing document page searching.
- Fix cabinet detail view pagination.
- Update project to work with Django 1.11.11.
- Fix deprecations in preparation for Django 2.0.
- Improve permission handling in the workflow app.
- The checkedout detail view permission is now required for the checked
  out document detail API view.
- Switch to a resource and service based API from previous app based one.
- Add missing services for the checkout API.
- Fix existing checkout APIs.
- Update API vies and serializers for the latest Django REST framework
  version. Replace DRF Swagger with DRF-YASG.
- Update to the latest version of Pillow, django-activity-stream,
  django-compressor, django-cors-headers, django-formtools,
  django-qsstats-magic, django-stronghold, django-suit, furl, graphviz,
  pyocr, python-dateutil, python-magic, pytz, sh.
- Update to the latest version the packages for building, development,
  documentation and testing.
- Add statistics script to produce a report of the views, APIs and test
  for each app.
- Merge base64 filename patch from Cornelius Ludmann.
- SearchModel retrun interface changed. The class no longer returns the
  result_set value. Use the queryset returned instead.
- Update to Font Awesome 5.
- Turn Mayan EDMS into a single page app.
- Split base.js into mayan_app.js, mayan_image.js, partial_navigation.js.
- Add a HOME_VIEW setting. Use it for the default view to be loaded.
- Fix bug in document page view. Was storing the URL and the querystring
  as a single url variable.
- Use history.back instead of history.go(-1).
- Don't use the previous variable when canceling a form action. Form now
  use only javascript's history.back().
- Add template and modal to display server side errors.
- Remove the unused scrollable_content internal feature.
- Remove unused animate.css package.
- Add page loading indicator.
- Add periodic AJAX workers to update the value of the notifications link.
- Add notification count inside a badge on the notification link.
- Add the MERC specifying javascript library usage.
- Documents without at least a version are not scanned for duplicates.
- Use a SHA256 hex digest of the secret key at the name of the lockfile.
  This makes the generation of the name repeatable while unique
  between installations.
- Squashed apps migrations.
- Convert document thumbnails, preview, image preview and staging files
  to template base widgets.
- Unify all document widgets.
- Display resolution settings are now specified as width and height and not
  a single resolution value.
- Printed pages are now full width.
- Move the invalid document markup to a separate HTML template.
- Update to Fancybox 3.
- Update to jQuery 3.3.1
- Move transfomations to their own module.
- Split documents.tests.test_views into base.py,
  test_deleted_document_views.py,
  test_document_page_views.py, test_document_type_views.py,
  test_document_version_views.py, test_document_views.py,
  test_duplicated_document_views.py
- Sort smart links by label.
- Rename the internal name of the document type permissions namespace.
  Existing permissions will need to be updated.
- Add support for OR type searches. Use the "OR" string between the terms.
  Example: term1 OR term2.
- Removed redundant permissions checks.
- Move the page count display to the top of the image.
- Unify the way to gather the project's metadata. Use mayan.__XX__ and
  a new common tag named {% project_information '' %}
- Return to the same source view after uploading a document.
- Add new WizardStep class to decouple the wizard step configuration.
- Add support for deregister upload wizard steps.
- Add wizard step to insert the document being uploaded to a cabinet.
- Fix documentation formatting.
- Add upload wizard step chapte.
- Improve and add additional diagrams.
- Change documenation theme to rtd.
- Fix carousel item height issues.
- Add the "to=" keyword argument to all ForeignKey, ManayToMany and OneToOne
  Fields.
- Add Makefile target to check the format of the README.rst file.
- Mark the feature to detect and fix the orientatin of PDF as experimental.
- Don't show documents with 0 duplicates in the duplicated document list.
- Clean up the duplicated document model after a document is deleted.
- Add support for roles ACLs.
- Add support for users ACLs.
- Add support for groups ACLs.
- Sort permission namespaces and permissions in the role permission views.
- Invert the columns in the ACL detail view.
- Fix issue #454. Thanks to Andrei Korostelev @kindkaktus for the issue and
  the solution.
- Update the role permission edit view require the permission grant or
  permission revoke permissions for the selected role.
- Only show the new document link if the user has access to create documents
  of at least one document type. GitLab Issue #302. Thanks to kg @kgraves.
- Support passing arguments to the document, document cache and document
  signatures storage backends. New settings:
  DOCUMENTS_STORAGE_BACKEND_ARGUMENTS,
  DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS,
  SIGNATURES_STORAGE_BACKEND_ARGUMENTS.
- Remove the setting STORAGE_FILESTORAGE_LOCATION. Document storage
  location for the storage.backend.filebasedstorage.FileBasedStorage
  backdend must now passed via the DOCUMENTS_STORAGE_BACKEND_ARGUMENTS,
  DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS, or
  SIGNATURES_STORAGE_BACKEND_ARGUMENTS if the backend is used to documents,
  the document image cache and/or document signatures. Use
  DOCUMENTS_STORAGE_BACKEND_ARGUMENTS = '{ location: <specific_path> }'
  If no path is specified the backend will default to
  'mayan/media/document_storage'.
- Standardize the way storages are used. All apps that use storage now define
  their storages in the .storages modules instead of the .runtime module.
  The storage.backends.filebasedstorage.FileBasedStorage has been remove,
  instead Django's default storage is used and each app is responsible
  of specifying their default path.
- Unify checkbox selection code for list items and table items.
- Add smart checkbox manager.
- Update Chart.js version.
- Improve line chart appearance. Fix mouse hover label issue.
- Add JavaScript dependency manager.
- Add support for passing arguments to the OCR backend.
- Fix issue when using workflows transitions with the new version
  upload event as trigger. Thanks to Sema @Miggaten for the find and
  the solution.
- Removing running workflow instances in document of a specific type if
  that document type is removed from the workflow.
- Make error messages persistent and increase the timeout of warning to 10
  seconds.
- Improve rendering of the details form.
- Update rendering of the readonly multiselect widget to conform to Django's
  updated field class interface.
- Add warning when using SQLite as the database backend.
- Use Mailgun's flanker library to process the email sources.
- Add locking for interval sources. This reduces the chance of repeated
  documents from long running email downloads.
- Add the option to enable or disable parsing when uploading a document
  for each document type.
- Add a new setting option to enable automatic parsing for each new
  document type created.
- Add support for HTML bodies to the user mailers.
- Production ALLOWED_HOSTS settings now defaults to a safer
  ['127.0.0.1', 'localhost', '[::1]']
- Capture menu resolution errors on invalid URLs. Closes GitLab issue #420.
- New environment variables: MAYAN_SECRET_KEY, MAYAN_CELERY_ALWAYS_EAGER,
  MAYAN_CELERY_RESULT_BACKEND, MAYAN_BROKER_URL, MAYAN_DATABASE_ENGINE,
  MAYAN_DATABASE_CONN_MAX_AGE, MAYAN_DATABASE_NAME, MAYAN_DATABASE_USER,
  MAYAN_DATABASE_PASSWORD, MAYAN_DATABASE_HOST, MAYAN_DATABASE_PORT,
  MAYAN_DEBUG.
- Stricter defaults. CELERY_ALWAYS_EAGER to False, ALLOWED_HOSTS to
  ['127.0.0.1', 'localhost', '[::1]'].
- New initialization command. Creates media/system and populates the
  SECRET_KEY and VERSION files.
- Sane scanner source paper source now defaults to blank.
- Merge Docker image creation back into the main repository.
- Docker image now uses gunicorn and whitenoise instead of NGINX to server
  the app and the static media.
- All installation artifact are now created and read from the media folder.
- Debian is now the Linux distribution used for the Docker image.
- Most Docker Celery workers are now execute using a lower OS priority number.
- Add COMMON_PRODUCTION_ERROR_LOGGING setting to control the logging of
  errors in production. Defaults to False.
- Change the error log file handle class to RotatingFileHandle to avoid an
  indefinitely growing log file.
- Disable embedded signatute verification during the perform upgrade command.
- Replace the DOCUMENTS_LANGUAGE_CHOICES setting option. Replaced with the
  new DOCUMENTS_LANGUAGE_CODES.
- Fix error when trying to upload a document from and email account with
  'from' and 'subject' metadata.
- Fix typo on message.header get from 'Suject' to 'Subject'.
- On multi part emails keep the original From and Subject properties
  for all subsequent parts if the sub parts don't specify them.
  Fixes issue #481. Thanks to Robert Schöftner @robert.schoeftner for the
  report and debug information.
- Don't provide a default for the scanner source adf_mode. Some scanners
  throw an error even when the selection if supported.
- Add a "Quick Download" action to reduce the number of steps to download
  a single document. GitLab issue #338.
- Recalculate a document's indexes when attaching or removing a tag from
  or to it.
- Recalculate all of a tag's documents when a tag is about to be deleted.
- Rename WizardStep class to DocumentCreateWizardStep to better reflect its
  purpose and interface.
