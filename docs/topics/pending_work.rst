===========
OCR backend
===========

Test writing
~~~~~~~~~~~~

All view and API tests must test each view in at least two ways:

- Object creations views must be tested with and without permissions.
- Object detail, list and delete views must be tested with and without
  object access.

All view and API tests must assert the status code of the response even
when the expected status if HTTP 200.


Pending tasks
-------------

These are task that need to be completed but are missing a dependency or
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

Caching
~~~~~~~
- Size limited caching. A new model in the common app will keep track
  of all cache files. A manager method will be provided that will
  return the cache files in other of age to be deleted.

Forms processing
~~~~~~~~~~~~~~~~
- Remove usage of self.cleaned_data. Use self.clean_data instead.

Metadata
~~~~~~~~
- Metadata lookup memory. Add a select2 style widget that will query a
  new metadata API endpoint that will return all used values so far.

Notifications
~~~~~~~~~~~~~
- Fix notification duplication of global & per document subscription
  notifications.

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

Sources
~~~~~~~
- Add ACLs support to sources.
- Provide error message/feedback when scanning from a remote scanner fails.
- Redirect to the same source when scanning from a remote scanner finishes.

Testing
~~~~~~~
- Add document test mixin that creates documents types and documents
  (to be used in dynamic_search.test_api).

UI
~~
- Shift click select to seletect multiple documents.
- During the document upload wizard and the option to double click to
  select document type and submit the form. The purpose is to speed up
  the step with less mouse travel since this is a common screen.
- Add metadata to the Menu class to allow UI code to decide where and how
  to display each menu.

Workflows
~~~~~~~~~
- Workflow trigger filters. Example: {{ document.document_type.name = 'invoice' }} or same
  UI as the smart links app. Will allow restricting the firing of workflow
  actions by an user defined filter criteria.
