4.0 (2021-XX-XX)
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
- Move the recently created document query calculation to it own model
