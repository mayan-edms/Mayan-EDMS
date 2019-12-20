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
- Remove the DOCUMENTS_DISABLE_BASE_IMAGE_CACHE,
  DOCUMENTS_DISABLE_TRANSFORMED_IMAGE_CACHE, and
  DOCUMENTS_FIX_ORIENTATION settings.
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
  signatures storage backends. New settings: DOCUMENTS_STORAGE_BACKEND_ARGUMENTS,
  DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS, SIGNATURES_STORAGE_BACKEND_ARGUMENTS
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
