============
Pending work
============

Release blockers
----------------

These are errors or issues that are blocking a release.

- None

Pending work
------------

These are tasks that need to be completed but are missing a dependency or
a design decision. As more information is added to each, they should be
converted into a MERC.

API
~~~
- User API edit view: Should not be able to add of remove groups without
  corresponding group access.
- User group list API get & post views: Should adding a group to an user
  via the API return 201 or 200. Currently returns 201.
- Consistent API return code for delete views without access. Some views
  return 403 other return 404.
- Update API docstrings. The upgrade to the latest DRF broke all formatting.
- Make views smaller. Much as much as possible to serializers.
- Switch to ViewSets.
- Add API filtering. Example unread notifications.


Documents
~~~~~~~~~
- Navigating to the interactive document page image is not triggering
  the document view event.


Events
~~~~~~
- New event: document emailed.


Forms processing
~~~~~~~~~~~~~~~~
- Remove usage of self.cleaned_data. Use self.clean_data instead.


Permissions
~~~~~~~~~~~
- Permission should be reciprocal. Example: To be able to add a tag to a
  document, the user must hold the tag add permission for the document
  and for the tag to be added. To be able to enable a metadata type to a
  document type, the user must hold the metadata add permissions for the
  metadata type and for the document type.
- Edit type permissions should only grant the ability to edit the properties
  of an object. To modify its relationship with other objects a reciprocal
  permission check should be instead.


Search
~~~~~~
- Rename SearchModel.pk to id


Sources
~~~~~~~
- Add ACLs support to sources.
- Provide error message/feedback when scanning from a remote scanner fails.
- Require a permission for document types to avoid a user that has the workflow
  creation permission to attach a workflow to a document type they don't
  control.
- Research making APIWorkflowDocumentTypeList a subclass of documents.api_views.APIDocumentTypeList
- A POST request to APIWorkflowDocumentTypeList should require some permission
  on the document type part to avoid adding non controlled document types
  to a new workflow.
- To transition a workflow, the transition permission is only needed for the
  workflow. Make it necesary to have the same permission for the document
  of document type.
- To view the transition log, the workflow view permission is only needed for the
  document. Make it necesary to have the same permission for the workflow or
  for the transition and the states.
- Render date time of scanned documents using SANE to a better output
  (like document versions).


Testing
~~~~~~~
- Add document test mixin that creates documents types and documents
  (to be used in dynamic_search.test_api).
- Update all API tests using self.client to just self. and the HTTP method.
- Add test for searches for each app that uses search.


UI - Frontend
~~~~~~~~~~~~~
- Fix menu not collapsing at the same width of nav parent.
- Move direct CSS style from code into base.css. grep 'style' * -R. Style code in:

    * appearance/templates/appearance/generic_list_items_subtemplate.html
    * appearance/templates/appearance/base.html
    * appearance/templates/appearance/generic_list_subtemplate.html
    * appearance/templates/navigation/generic_link_instance.html

- Check if location is found in partial and remove it. Avoid circular loading.
- Add location to history after a form submit redirect.


UI
~~
- Shift click select to seletect multiple documents.
- During the document upload wizard and the option to double click to
  select document type and submit the form. The purpose is to speed up
  the step with less mouse travel since this is a common screen.
- Add metadata to the Menu class to allow UI code to decide where and how
  to display each menu.
- Reduce the facet buttons paddings.
- Make facet action button smaller. Reduce margin-bottom.
- Remove previous from the views.py. It is not longer used by the form's cancel button.


Workflows
~~~~~~~~~
- Workflow trigger filters. Example: {{ document.document_type.name = 'invoice' }}
  or same UI as the smart links app. Will allow restricting the firing of workflow
  actions by an user defined filter criteria.
- Require a permission for document types to avoid a user that has the workflow
  creation permission to attach a workflow to a document type they don't
  control.
- Research making APIWorkflowDocumentTypeList a subclass of
  documents.api_views.APIDocumentTypeList
- A POST request to APIWorkflowDocumentTypeList should require some permission
  on the document type part to avoid adding non controlled document types
  to a new workflow.
- To transition a workflow, the transition permission is only needed for the
  workflow. Make it necesary to have the same permission for the document
  of document type.
- To view the transition log, the workflow view permission is only needed for
  the document. Make it necesary to have the same permission for the workflow or
  for the transition and the states.


New features
------------


API
~~~
- Add converter API
- Document signatures API
- Smart settings API
- Use REST_API's 'mayan_permission_attribute_check' to simplify API views access checking and filtering.
- DRF filtering using the URL query.


Converter
~~~~~~~~~
- New zoom transformation. Resample, not just bigger final size but do
  a resize * zoom multiple before. Produces a bigger image or higher
  quality than the original.


Caching
~~~~~~~
- Size limited caching. A new model in the common app will keep track
  of all cache files. A manager method will be provided that will
  return the cache files in other of age to be deleted.


Distribution
~~~~~~~~~~~~
- Python based Javascript package manager. Each app specifies what
  library and version needs. The common app (or a new app) will add all
  the JS loading lines automatically so that compress can detect them.


Metadata
~~~~~~~~
- Metadata lookup memory. Add a select2 style widget that will query a
  new metadata API endpoint that will return all used values so far.
- Metadata validation_choices and parser_choices as static model methods
- Metadata.api as Metadata.utils and manager


Search
~~~~~~
- Add support for highlighting the search results in pages.


Settings
~~~~~~~~
- Database based settings.


Sources
~~~~~~~
- UI improvement for staging folders files selection. GitLab issue.


UI
~~
- Upgrade to Bootstrap 4.
- Upgrade to Flatly 4.
- Better workflow transition UI. Instead of a dropdown show all the
  available transitions as buttons.


Workflows
~~~~~~~~~
- Workflow trigger filters. Example: {{ document.document_type.name = 'invoice' }} or same
  UI as the smart links app. Will allow restricting the firing of workflow
  actions by an user defined filter criteria.
- New workflow action: send email. Subject and content are templates.


Other
~~~~~
- Python based Javascript package manager. Each app specifies what
  library and version needs. The common app (or a new app) will add all
  the JS loading lines automatically so that compress can detect them.
- When moving documents to the trash update the message to "submitted"
  and not "moved" or "deleted" since this is handled by a task queue
  and is not immediate and doesn't delete the document.
- When emptying the trash update the message to "submitted"
  since this is handled by a task queue and is not immediate.
- New app that allows creating user document filters. Will provide the
  same service as the document filters class. Interface can be made
  using the template language or the same UI as the smart links.
- Allow add queue metadata that can be exported via a management command.
  This will allow creating supervisor templates without all the worker
  entries being hardcoded.
- Delete .gitignore files from copied packages. Include .gitignore files
  keep compiled or distributable files from being included in the main
  repository. Temporary measure until a Javascript library manager is
  added.
- Automatically capture license information from installed Javascript
  libraries.
- Automatically capture license information from installed Python
  packages.
- Update celery to 4.1.0
- Update to use the new class based views in the authentication app.
  password_change(), password_change_done(), password_reset(),
  password_reset_done(), password_reset_confirm(), and password_reset_complete()
  function-based views are deprecated in favor of new class-based views
  PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
  PasswordResetDoneView, PasswordResetConfirmView, and PasswordResetCompleteView.
- django.utils.translation.string_concat() is deprecated in favor of
  django.utils.text.format_lazy(). string_concat(strings) can be
  replaced by format_lazy('{}' x len(strings), strings).
  Found in converter/classes.py and metadata/forms.py.
- Fix warnings in preparation for Django 2.0.
- Update all tempfile.mkstemp() to tempfile.mkstemp(dir=setting_temporary_directory.value)
- Get rid of common.utils.get_descriptor only used by common.utils.copyfile
- Update common.utils.copyfile to use only file objects.
- Change metadata label column from CharField to Label
- Start testing to Python 3 compatibility.
- Unify all RelationshipForms into a common class.
- Add test for event subscription view.
- Repeated templates: password_reset_confirm.html and password_reset_form.html
- Remove unused text=get_notification_count from events.links
- Reduce number of languages so dropzone view starts faster.
- In DocumentComment model, rename comment field to text.
- class MultipleInstanceActionMixin is deprecated. Replace views using this with
  MultipleObjectFormActionView or MultipleObjectConfirmActionView
- Subscribe to tag events
- Subscribe to workflow events
- Subscribe to workflow state events
- Link to go from event notification to view. Example document workflow notification to document workflow views.
- Find replacement for ``python-gnupg``. Unstable & inconsistent API.
- New app that allows creating user document filters. Will provide the
  same service as the document filters class. Interface can be made
  using the template language or the same UI as the smart links.
- Allow add queue metadata that can be exported via a management command.
  This will allow creating supervisor templates without all the worker
  entries being hardcoded.
- Automatically capture license information from installed Javascript
  libraries.
- Automatically capture license information from installed Python
  packages.
- Finish and merge improved compressed file branch.
- Improve and merge PCL support branch.
- Swtich to self hosted documentation.
- Unify error logs in a common model. Fields: Datetime, namespace,
  message, content type, object id.
- Export documents as PDF. Each document image is used to create a PDF
  dinamycally.
- Document splitting. Only for PDF files first. A document versions
  relationship between the documents has to be designed.
- Manually linking documents.
- Migrate settings/base.py to Django's 1.11 format.
- Rename model methods to use ``get_`` or ``do_``
- Hunt TODO
- Hunt FIXME
- Convert SETTING_GPG_BACKEND into a setting option similar to converter and converter options.
- Reorganize modelForms Meta class and methods.
- Periodic messages, like notifications. Using an AJAX worker.
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
