4.0 (2021-02-XX)
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
  viceversa.
- A method decorator was added to the lock manager app to ease usage of the
  same lock workflow in methods of the same class.
- The error handling of the ``CachePartitionFile`` methods was improved.
  This ensures proper clean up of stray storage files on model file creation
  error. The model now avoids accessing the model file for clean up on model
  file creation error, which would raise a hard to understand and diagnose
  missing file entry error. The model now avoids updating cache size on
  either model or storage file creation error.
- Support disabling form help texts via ``form_hide_help_text``.
