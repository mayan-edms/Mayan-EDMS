4.0.15 (2021-08-07)
===================
- Improve the document version export API endpoint.

  - Enable tracking the user and persisting the value for the events.
  - Change the view class form a custom mixin to be a subclass of
    `generics.ObjectActionAPIView` one.
  - Improve test to check for message creation after export.
  - Avoid returning an error when using the `GET` method for the view.

- Improve the `generics.ObjectActionAPIView` class.

  - Merge with `ActionAPIViewMixin`.
  - Add `action_response_status` for predetermined status codes.
  - Add message when the `.object_action` method is missing.

- Fix the view to mark all messages as read.
- Track the user when marking messages as read or unread.
- Fix action messages.    

4.0.14 (2021-08-05)
===================
- Fix a regression in the document version page image cache maximum size
  setting callback.
- Fix converter layer priority exclusion for layers with a priority of 0.
  This fixes the preview layer priority when editing the redactions of pages
  that also contain transformations in other layers.

4.0.13 (2021-08-02)
===================
- Checkout test updates.

  - Silence debug output of tests.
  - Speed up tests using document stubs.

- Improve organization URL and host settings. Closes GitLab issues
  #966 and #1002. Thanks to None Given (@nastodon) and
  Bw (@bwakkie) for the reports.

  - Patch Django's HttpRequest object to override scheme
    and host.
  - Fix organization setting used to set the REST API URL
    base path.

- Track user for event when submitting a document version for OCR.
- Fix OCR version event texts.
- Update the document index list and document cabinet list links to require
  the same permission scheme as the views they reference.
- Add the document creation date time as a search field.

4.0.12 (2021-07-19)
===================
- Fix main menu active entry handling.
- Fix ID number in ``document_url`` attribute of the ``DocumentFile``
  and ``DocumentVersion`` serializers. Thanks to forum user @qra for the
  report. Topic 5794.
- Add API endpoint to display the list of valid transition options for a
  workflow instance. Thanks to forum user @qra for the report. Topic 5795.
- Add the workflow template content to the workflow instance API schema.
  Thanks to forum user @qra for the request. Topic 5795.
- Clarify purpose of project settings.
- Minor API serializer cleanups.
- Add explicit cabinet serializer read only fields.
- Fix multi scope search result initialization. Closes GitLab issue #1018.
  Thanks to Ryan Showalter (@ryanshow) for the report.
- Detect and report when a search scope does not specify a query.

4.0.11 (2021-07-06)
===================
- Update date time copy code from migration document:0063 to work with
  database that store time zone information and those that don't.
- Switch deployment instructions to use ``venv`` instead of ``virtualenv``.
- Add support for using local PIP cache to build Docker images.
- Add a Vagrant setup for testing. Integrates project
  https://gitlab.com/mayan-edms/mayan-edms-vagrant. Closes GitLab issue
  #937. Thanks to Max Kornyev (@mkornyev) for the report.
- Improve ``user_settings_folder`` variable creation. Works with
  ``MEDIA_ROOT`` paths with and without a trailing slash.
- The GitLab CI upgrade tests now update a test document to populate the
  older version install and trigger more migration code paths.
- Update all shell usage from ``bash`` to ``sh``. ``sh`` symlinks to ``dash``
  in the Docker image. This also expands the usability of the supervisor
  file for direct deployments in more operating systems. Closes GitLab
  issue #1013. Thanks to joh-ku (@joh-ku) for the report.
- Replace the ``wait.sh`` file with a Python alternative that can wait on
  network ports or PostgreSQL directly as a client.
- Upgrade ``supervisord`` from Debian buster version 3.3.5-1 to Debian
  bullseye version 4.2.2-2. This version uses Python3 and was the last
  dependency that required installing Python2 in the Docker image.
- Add the ``id`` field as sortable field in all the API that have ordering
  enabled.

4.0.10 (2021-07-02)
===================
- Simplify code block to delete OCR content of a document version.
- Make document version timestamp time zone aware before copying them over
  during migration.
- Split duplicates migration query into two separate queries to increase
  compatibility with database managers.
- Add support to the GitLab CI for local apt proxies.

4.0.9 (2021-06-29)
==================
- Improve scope search.

  - Support more than two source scopes per operator.
  - Support ``match_all`` logic per scope.
  - Support returning a single scope without using the operator output.
  - Disable search limits when multiple scopes are specified.
  - Add separate query decoding method.

- Increase the padding of the main menu panel anchors. Closes GitLab issue
  #1004. Thanks to Bw (@bwakkie) for the report.
- Rotate the main menu accordion indicator when opened or closed.
- Optimize jQuery usage of the $(this) object. Remove some unused jQuery
  code from the document card update methods.
- Add more uses of ``update_fields`` to ``.save()`` methods.
- Simplify logic using the document parser content update using
  ``update_or_create``.
- Raise document list errors on debug or testing.

4.0.8 (2021-06-23)
==================
- Update PIP to version 21.1.2.
- Use longer version of the Celery worker option.
- Make optional the `user_id` argument of
  `task_document_file_page_image_generate`.
- Another round of worker queue assignments tuning.
- Simplify the GPG temporary home preparation. A temporary directory context
  manager is now used that also guarantees that the temporary folder will be
  removed even on failures.
- Don't assume all signatures provide a ``date_time`` field.
- Optimize file and version page image API. Load the page object only once
  per request.
- Unify the supervisord templates. The direct deployment and the Docker image
  now use the same supervisord template.
- Email the active document version. Instead of emailing the latest updated
  document file, the document emailing with attachment will now export the
  active version and email that as an attachments. This mimics more closely
  the existing behavior of this feature before the document version were
  separated into versions and files.
- Update Django version 2.2.23 to 2.2.24.
- Improve Docker Compose installation and upgrade instructions.
- Fix the document type button not appearing. Update the cascade condition
  of the document type setup link to display when there are not document
  types created.
- Don't cache the missing items template to allow it to be removed when
  the missing items are fixed.
- Event testing improvements for several apps.
- The date and time of document version timestamps are now carried over
  during the upgrade from version 3.5.x to 4.0.x.
- Update the file metadata submit actions to keep track of the user and apply
  it to the events.
- Update the document parsing submit actions to keep track of the user and
  apply it to the events.
- Apply small optimization to ``MultipleObjectViewMixin``
  ``.get_object_list()`` method. The method now reuses the existing
  ``pk_list`` variable.
- Fixed an issue with the document metadata add and edit actions which
  prevented the user value to be ignored at the event commit.
- Convert the GitLab CI and Dockerfile into platform templates.
- Update Docker base image from Debian:10.8-slim to Debian:10.10-slim.
- Add config entry ``DEFAULT_USER_SETTINGS_MODULE``.
- Add serializer explicit read only fields.
- Optimize documents app saves with `update_fields`.

4.0.7 (2021-06-11)
==================
- Fix typo in the CELERY_MAX_TASKS_PER_CHILD_ARGUMENT environment
  variable.

4.0.6 (2021-06-10)
==================
- Fix celery argument names in supervisord template. Set correct attribute
  names max-tasks-per-child and max-memory-per-child when starting celery
  workers. Closes #998. Thanks to joh-ku (@joh-ku) for the report and patch.
- Use different environment when composing the child limits arguments.
  Update CELERY_MAX_MEMORY_PER_CHILD and CELERY_TASKS_MEMORY_PER_CHILD
  to use a separate argument variable, like CELERY_CONCURRENCY.

4.0.5 (2021-06-08)
==================
- Turn the release notes upgrade instructions into a partial template.
- Add support for Celery's max memory and tasks. Support
  ``--max-memory-per-child`` and ``--max-tasks-per-child`` using
  the environment variables ``MAYAN_WORKER_X_MAX_MEMORY_PER_CHILD``
  and ``MAYAN_WORKER_X_MAX_TASKS_PER_CHILD``.
- Add commented Docker compose database port entry.
- Support Gunicorn's ``--limit-request-line`` via the
  ``MAYAN_GUNICORN_LIMIT_REQUEST_LINE`` environment variable.
- Improve the Docker image environment variables chapter. Include missing
  variables and automate displaying the default values of several.
  Organize variables by topic.
- Exclude trashed documents from the workflow runtime proxy document count.
- Fix metadata form ``KeyError`` exception when required metadata is missing.
  Closes GitLab issue #997. Thanks to Raimar Sandner (@PiQuer) for the report
  and debug information.
- Document file and version page image updates:

  - Improve document version page base image cache invalidation on source
    image transformation updates.
  - Optimize transformation list generation by replacing several loops with
    list extensions.
  - Avoid using the source content transformations when calculating the
    document version transformation list hash. This cause duplicated document
    version page transformation in some cases. Closes GitLab issue #996.
    Thanks to Reinhard Ernst (@reinhardernst) for the report and debug
    information.
  - Improve document version page image API URL hash uniqueness generation.
    Ensure browsers do not use a cached document version page image when
    the transformations of the source object of the version are updated.

4.0.4 (2021-06-05)
==================
- Merge updates from version 3.5.10

  - Remove event decorator database transaction
    Solves workflows not being launched on document creation. Closes
    GitLab issue #976 and issue #990, thanks to users Megamorf (@megamorf),
    A F (@adzzzz) for the reports and debug information.

4.0.3 (2021-06-03)
==================
- Merge updates from version 3.5.9

  - Fix user model theme related field error after deleting a theme already
    assigned to a user. Closes GitLab issue #972. Thanks to Niklas Maurer
    (@nmaurer) for the report.
  - Add duplicate document tool tests.
  - Speed up some OCR view tests.
  - Add explicit Docker logout repository in CD/CI jobs.
  - Fix permission required for the document content error list link to match
    the permission required for the document parsed content error list view.
    GitLab issue #954. Thanks to Ilya Pavlov (@spirkaa) for the report.
  - Fix permission required for the OCR content delete link to match the
    permission required for the OCR content delete view. GitLab issue #954.
    Thanks to Ilya Pavlov (@spirkaa) for the report.

- Update dependency versions:

  - django-solo from version 1.1.3 to 1.1.5.
  - python-magic from version 0.4.15 to 0.4.22

- Makefile updates

  - Unify Docker test with staging targets.
  - Replace underscore in target names with hyphen for uniformity.
  - Add Redis Docker test targets.

- Lock manager updates

  - Rename get_instance() method to get_backend(). This method
    returns a class and not an instance.
  - Add management command tests.
  - Add optional _initialization method for backends.
  - Update the RedisLock backend to use a connection pool.

- Update Docker entrypoint template to support default worker
  concurrency values. Now correctly passes the default concurrency
  value of the D class worker.
- Updated REST API examples for version 4 of the API.

4.0.2 (2021-05-25)
==================
- Messaging app updates:

    - Add links to set messages as unread.
    - Automatically set messages as read upon accessing them. GitLab issue
      #981, thanks to Ilya Pavlov (@spirkaa) for the report.
    - Disable links to mark messages as read or unread based on the state of
      the message.

- Clarify Redis and Lock manager upgrade steps.
- Action dropdown template updates:

  - Move dropdown template partial to the navigation app.
  - Remove unused {{ link_extra_classes }}.
  - Remove obsolete dropdown HTML markup.

- Fix action menu disabled link appearance.
- Correct user_settings folder creation step. Closes GitLab issue #984.
  Thanks to Matthias Löblich (@startmat) for the report.
- Ensure the API authentication has completed before doing initial filtering.
  Fixes API views returning 404 errors when using token authentication.
- Minor source string fixes.
- Update Django REST framework from version 3.11.0 to 3.11.2.
- Update PIP from version 21.0.1 to 21.1.1.
- Update django-mptt from version 0.11.0 to 0.12.0.
- Add ordering to cabinets. Closes GitLab issue #986. Thanks to Hanno Zulla
  (@hzulla) for the report.

4.0.1 (2021-05-20)
==================
- Fix group and user setup link conditional disable not working as
  expected.
- Fix Docker environment variables documentation chapter regarding
  worker concurrency.
- Add troubleshooting section regarding document file access after upgrade
  to version 4.0.
- Allow migration of the settings ``DOCUMENTS_STORAGE_BACKEND`` and
  ``DOCUMENTS_STORAGE_BACKEND_ARGUMENTS`` for more situations.

4.0 (2021-05-19)
================
- Add document version page list reset.
- Add document version page delete.
- Add document version hash from content object.
- Improve file and version page max page calculation.
- Add version page navigation.
- Support document file deletion.
- Move document download code to document file.
- Add document file permissions.
- Move page count update to document file.
- Several renames for consistency. Use the major, minor, verb order
  for variable names in more places.
- Point document to latest document version. This removes the document page
  views and makes them aliases of the document version pages views.
- Add document version deletion.
- Add document file properties view.
- Remove page disabling/enabling.
- Add document version page model.
- Add caches, settings and handlers for the document version cache.
- Add document version page image API.
- Rename ``DocumentPage`` model to ``DocumentFilePage``.
- Invert the document and OCR migrations dependency. Makes the OCR migration
  dependent on the documents app migration. This allows disabling the OCR app.
- New event ignore and keep attribute options
- No results template for file list view.
- Fixed version page append
- Convert document model save method to use event decorator.
- Update file hooks to work when there is not previous file.
- Remove all remaining orientation support. Remove rotation test files.
- Add multi document version delete.
- Add a generic multi item delete view.
- Longer document file action texts.
- Document stub recalculation by file save and delete
- Better document version page remap
- Reorganize and split document model tests
- Add file upload mixin method.
- Unify the action dropdown instances into a new partial called
  ``appearance/partials/actions_dropdown.html``.
- Move the ``related`` menu from the "Actions" to the ``facet`` area.
- Add sources to their own menu.
- Add ``mode`` argument to SharedUploadedFile.
- Split document app model tests into separate modules.
- Split document app test mixins into separate modules.
- Fix the appearance of the automatically generated view titles.
- Add a new "Return" menu for secondary object views.
- Use the "Return" menu for the document version, document version page,
  document file, and document file page views.
- Remove the "File..." reference to the document file form fields as these
  are now obvious.
- Add more return links. From document version to version list, from
  document file to document file list, from document version page to
  document, from document file page to document.
- Add document version edit view. Allows editing the document version comment.
- Improve the return links with the chevron as the uniform secondary icon.
- Rename the document view, document version view and document file views to
  document preview, document file preview and document version preview.
- Enable more cabinets, checkouts, document comments, metadata, linking,
  mailer, mirroring, web links apps.
- Allow using staging folders for new document file uploads.
- Add conditional source link highlighting.
- Add document version create view and permission.
- Add validation and test for repeated document version page numbers.
- Improve page remap code and add annotated content object list support.
- Don't display the file upload link on the document file delete view.
- Update shared upload file to allow storing the original filename.
- Upload the new document file upload code path to conserve the original
  filename.
- Rename ``DeletedDocument`` to ``TrashedDocument``, same with the
  corresponding trashed fields and manager methods.
- Add document file download event.
- Rename all instances of ``icon_class`` to ``icon`` as only icon instances
  are used now in every app.
- Add icons to the mark notification as seen and mark all notification as
  seen links.
- Switch both view to mark notification as read to use the POST request
  via a confirmation view.
- Return the event type subscription list sorted by namespace label and event
  type label.
- Make the search fields more uniform and add missing ones.
- Add full label for search parent fields.
- Add events for the document type quick label model.
- Add dedicated API endpoints for the document type quick label model.
- Update the file cache partition purge view to be a generic view that can
  be called using the content type of an object. Adds a new file cache
  partition purge permission.
- Added ``ContentTypeTestCaseMixin``.
- Include ``EventTestCaseMixin`` as part of the base test case mixin.
- Rename usage of "recent document" to the more explicit "recently
  accessed document". This was done at the mode, view and API level.
  The recently accessed document API will now require the document view
  permission.
- Rename the document model ``date_added`` field to ``datetime_created`` to
  better reflect the purpose of the field.
- Add a ``RecentlyCreatedDocument`` proxy and associate the recent document
  columns to it.
- Move the recently created document query calculation to its own model
  manager.
- Add the recently created document API.
- Add favorite documents API.
- Rename the ``misc_models.py`` module to ``duplicated_document_models.py``.
- Split the ``document_api_views.py`` modules into ``document_api_views.py``
  and ``trashed_document_api_views.py``.
- Add date time field to the favorite documents models to ensure deterministic
  ordering when deleting the oldest favorites.
- Rename the setting ``DOCUMENTS_RECENT_ACCESS_COUNT`` to
  ``DOCUMENTS_RECENTLY_ACCESSED_COUNT``, and ``DOCUMENTS_RECENT_ADDED_COUNT``
  to ``DOCUMENTS_RECENTLY_CREATED_COUNT``. Config file migrations and
  migration tests were added. Environment and supervisor settings need to be
  manually updated.
- Document stubs without a label will now display their ID as the label.
  This allows documents without files or versions to be accessible via the
  user interface.
- Add the reusable ObjectActionAPIView API view. This is a view that can
  execute an action on an object from a queryset from a POST request.
- Improve proxy model menu link resolution. Proxy model don't need at least
  one bound link anymore to trigger resolution of all the parent model links.
  The inclusion logic is now reverse and defaults to exclusion. Menu need to
  be configured explicitly enable to proxy model link resolution using the new
  ``.add_proxy_inclusions(source)`` method.
- Move the duplicated documents code to its own app.
- Add duplication backend support to the duplicates app.
- Add duplicates app API.
- Add support for search model proxy registration.
- Remove the ``views`` arguments from the SourceColumn class. Use models
  proxies instead to customize the columns of a model based on the view
  displayed.
- Add document type change workflow action.
- Rename WizardStep to DocumentCreateWizardStep. This change better reflects
  its purpose and interface.
- Move DocumentCreateWizardStep to the sources.classes module.
- Add automatic loading support for the ``wizard_step`` modules. It is no
  longer necessary to import these modules inside the App's .ready() method.
- Update API endpoints to use explicit primary key URL keyword arguments.
- Split workflow models module into separate modules.
- Remove usage of Document.save(_user). The event_actor attribute is used
  instead.
- Convert the key creation and expiration fields to date and time fields.
- Add creation and download events for keys.
- Add event subscription for keys.
- Include time of document signatures. Closes GitLab issue #941. Thanks
  to forum user Tomek (@tkwoka) for the report and additional
  information.
- Add document signature tool to refresh the content of existing signatures
  when there are database or backend changes.
- Moved ``ObjectLinkWidget`` to the views app.
- Add global ACL list view.
- ``appearance_app_templates`` now passes the request to the templates being
  rendered.
- Remove the user impersonation fragment form the ``base.html`` template and
  moved it to its own viewport template.
- Enable subscribing to user impersonation events.
- Enable impersonation permission for individual users.
- Allow impersonating users from the user list view.
- Update jQuery from version 3.4.1 to 3.5.1.
- Move user language and timezone code from the `common` app to a new app
  called `locales`.
- Move common and smart settings app `base` template markup to their own
  apps via the `viewport` app template.
- Rename document comment model's `comment` field to `text`.
- Support sorting document comments by user or by date.
- Increase the size of the ``Lock`` lock manager model ``name`` field to a
  255 char field. Closes GitLab issue #939. Thanks to Will Wright
  (@fireatwill) for the report and investigation.
- Add example usage for the ``COMMON_EXTRA_APPS`` and
  ``COMMON_DISABLED_APPS``. Closes GitLab issue #929. Thanks to Francesco
  Musella (@francesco.musella-biztems) for the report.
- Reorganize mixins. Add a suffix to specify the purpose of the mixin and
  move them to different module when appropriate.
- Refactored the notification generation for efficiency, scalability and
  simplicity. Only users subscribed to events are queued for notifications.
  Content types of event targets and action objects is reused from the action
  model instead of gathering from inspection. Nested loop removed and lowered
  to a single loop.
- Optimize SourceColumn resolution. Support column exclusion for all object
  types. Ensure columns are not repeated when resolved even if they were
  defined multiple times. Improve docstring for the resolution logic in each
  level. Remove unused ``context`` parameter. Add SourceColumn tests.
- Support defining the default ``SearchModel``. This allows removing the hard
  coded search model name from the search template and allows third party
  apps to define their own default ``SearchModel``.
- Update MySQL Docker image from version 5.7 to 8.0. PostreSQL image from version
  10.14 to 10.15. Redis image from version 5.0 to 6.0.
- Move time delays from test and into its own test mixin. Remove MySQL test delays.
- Standardize a class for the widgets of the class ``SourceColumn`` named
  ``SourceColumnWidget``.
- The cabinet view permission is now required for a document, to be able to
  view which cabinets contain that document. This change mirrors the
  permission layout of the metadata and tag apps.
- File caching now uses the same lock for all file methods. This ensures that
  a cache file that is being deleted or purge is not open for reading and
  vice versa.
- A method decorator was added to the lock manager app to ease usage of the
  same lock workflow in methods of the same class.
- The error handling of the ``CachePartitionFile`` methods was improved.
  This ensures proper clean up of stray storage files on model file creation
  error. The model now avoids accessing the model file for clean up on model
  file creation error, which would raise a hard to understand and diagnose
  missing file entry error. The model now avoids updating cache size on
  either model or storage file creation error.
- Support disabling form help texts via ``form_hide_help_text``.
- Docker image tagging layout has been updated. Images are tagged by version
  and series. Series have the 's' prefix and versions have the 'v' prefix.
- Added API endpoints for the Assets model.
- Added cached image generation for assets.
- Added asset detail view with image preview.
- Added a detail view for the cache model.
- Added the ``image_url`` field to the Workflow template serializer.
- Added retry support for the workflow preview generation task.
- Updated the autoadmin app to use the login template ``login_content``
  template hook. This allows the autoadmin app to show login information
  without directly modifying the login template.
- Update tags app to improve user event tracking on view and API.
- Support deleting multiple document files.
- Track document file deletion event user in views.
- Rename ``setting_workflowimagecache_storage`` to
  ``setting_workflow_image_cache_storage_backend``.
- Support collapsing the options of the menus "list facet" and "object" when
  in list view mode. This behavior is controlled with the new settings:
  ``COMMON_COLLAPSE_LIST_MENU_LIST_FACET`` and
  ``COMMON_COLLAPSE_LIST_MENU_OBJECT``. Both default to ``False``.
- Added a check to the task manager app to ensure all defined tasks are
  properly configure in their respective ``queues.py`` modules.
- ACL apps updates: Add ACL deleted event, track action actor in API and
  views. Simply API views using REST API mixins. Update API views to return
  404 errors instead of 403, move global ACL list to the setup menu,
  model that are registered for ACLs are now also automatically register
  events in order to receive the ACL deleted event, improve tests and add more
  test cases.
- Update AddRemoveView to only call the underlying add or remove methods only
  if there are objects to act upon instead of calling the method with an
  empty queryset which would trigger unwanted events.
- Add ``ExternalContentTypeObjectAPIViewMixin`` to the REST API app. This
  mixin simplifies working with models that act upon another object via
  their Content Type, such as the ACLs.
- Update the ACL app to support multiple foreign object permission
  inheritance. Support for ``GenericForeignKey`` non default ``ct_field``,
  and ``fk_field`` was also added.
- Added support to export the global events list, object events list and
  user events list.
- Registering a model to receive events will cause it to have the object
  event view and object event subscription links bound too. This can
  be disabled with the `bind_links` argument. The default menu to bind the
  links is the "List facet". This can be changed via the ``menu`` argument.
- Change the format of the ``file_metadata_value_of`` helper. The driver
  and metadata entry are now separated by a double underscore instead of a
  single underscore. This allows supporting drivers and entries that might
  contain an underscore themselves.
- Add ``databases`` app to group data and models related code.
- Add class support for scoped searches. GitLab issue #875.
- Add sorting support to the API.
- Updated how the user interface column sorting works. The code was
  simplified by using a single query variable. The code was expanded
  to support multiple fields in the future. The URL query key used for
  column sorting was changed to match the API sorting.a
- Added the ``databases`` app. This app groups data and models related code.
- Added a patch for Django's ``Migration`` class to display time delta for
  each migration during development.
- Docker Compose updates:

    - Use profiles for extra containers.
    - Converted to use extensions to remove duplicated markup.
    - A new container was added to mount an index.
    - Added support for Traefik.
    - Added sample .env file.
    - Update required Docker Compose to version 1.28.

- Add a third document filename generator that used an UUID plus the original
  filename of the uploaded file. This generator has the advantage of producing
  unique filename while also preserving the original filename for reference.
- Add support for the "Reply To" field for sending documents via email and
  for the mailing workflow actions. Closes GitLab issue #864. Thanks to
  Kevin Pawsey (@kevinpawsey) for the request.
- Allow customization of the error condition when generating document images.
  This allows displaying more icons in addition to the generic document
  image error with additional contextual information and popup messages
  explaining the actual error condition.
- Add key attributes to the document signature serializers. Forum topic 5085.
  Thanks to forum user @qra for the request.
- Added key attributes to the document signature model as calculated
  properties.
- Move detached signature upload from the created endpoint to a
  new /uploaded endpoint.
- Added document signature events.
- Refactored the workflows app.

    - Rebalance permissions needed to transition a workflow instance.
      The workflow instance transition permission is now needed for
      the document and for either the transition or the workflow.
    - Add more tests including trashed document tests.
    - Split API tests into instance and template tests.
    - Add `workflow-instance-log-entry-detail` end point.
    - Add parent URL fields to serializers.
    - Allow passing extra data when transitioning a workflow via the API.
    - Limit state options to workflow when using the API. This matches
      the UI behavior.

- Renamed the AddRemove view ``main_object_method_add`` to
  ``main_object_method_add_name`` and ``main_object_method_remove`` to
  ``main_object_method_add_remove_name``.
- Add ``has_translations`` flag to MayanAppConfig to indicate if the app
  should have its translation files processed or ignored. Defaults to
  ``True``.
- Dependency version upgrades:

  - coverage from 5.1 to 5.5.
  - Django to 2.2.23.
  - django-debug-toolbar to 3.2.
  - django-extensions to 3.1.2.
  - django-rosetta to 0.9.4.
  - django-silk to 4.1.0.
  - flake8 to 3.9.0.
  - ipython to 7.22.0.
  - pycounty to 20.7.3.
  - requests to 2.25.1.
  - Sphinx to 3.5.4.
  - sh to 1.14.1.
  - sphinx-autobuild to 2021.3.14.
  - sphinx-sitemap to 2.2.0.
  - sphinxcontrib-spelling to 7.1.0.
  - tornado to 6.1.
  - tox from 3.14.6 to 3.23.1.
  - transifex-client to 0.14.2.
  - twine to 3.4.1.
  - wheel to 0.36.2.

- Fix sub workflow launch state action.
- Convert the workflow instance creation to a background task.
- File caching app updates

  - Add cache partition purge event.
  - Use new event decorator.
  - Use related object as the cache partition purge event action object.
  - Allow cache prune to retry on LockError.
  - Add maximum cache prune failure counter.
  - Remove possible cache file lock name collision.

- Add locking to the duplicated document scan code to workaround race
  condition in Django bug #19544 when adding duplicated documents via
  the many to many field ``.add()`` method.
- Remove the default queue. All tasks must now be explicitly assigned to an
  app defined queue.
- Update file cache to use and LRU style eviction logic.
- Only prune caches during startup if their maximum size changed.
- Add detection of excessive cache pruning when cache size is too small for
  the workload.
- Detect and avoid duplicated queue names.
- Add a fourth class of worker.
- Re-balance queues.
- Rename workers from ``fast``, ``medium``, and ``slow`` to ``A`` (fast),
  ``B`` (new workers), ``C`` (medium), ``D`` (slow).
- Add support for passing custom nice level to the workers when using the
  Docker image ``run_worker`` command. The value is passed via the
  ``MAYAN_WORKER_NICE_LEVEL`` environment variable. This variable defaults to
  ``0``.
- Avoid adding a transformation to a layer for which it was
  not registered.
- Add LayerError exception.
- Fix redaction ACL support.
- Add support for typecasting the values used to filter the ACL object
  inherited fields.
- Rename the ``mayan_settings`` directory, which is used to allow custom
  setting modules, to the more intuitive ``user_settings``.
