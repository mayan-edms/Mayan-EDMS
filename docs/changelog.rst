2011-10-05
----------
* Initial translation to Portuguese

2011-08-19
----------
* Added improved documentation

Version 0.8.3
-------------

* Added a Contributors file under the docs directory
* Moved the document grouping subtemplate windows into a document
  information tab
* Change the mode the setup options are shown, opting to use a more of a
  dashboard style now
* Changed the tool menu to use the same button layout of the setup menu
* Moved OCR related handling to the tools main menu
* Improved the metadata type and metadata set selection widget during
  the document upload wizard
* Added a view to the about menu to read the LICENSE file included with
  Mayan
* Added converter backend agnostic image file format descriptions
* Disable whitelist and blacklist temporarily, removed document_type
  field from interactive sources
* Fully disabled watch folders until they are working correctly
* Updated the project title to 'Mayan EDMS'
* If ghostscript is installed add PDF and PS to the list of file formats
  by the python converter backend
* Use Pillow (http://pypi.python.org/pypi/Pillow) instead of PIL

  - Pillow is a fork of PIL with several updated including better jpeg and png library detection
  - Users must uninstall PIL before installing Pillow
   
* Updated the static media url in the login excempt url list
* Added remediatory code to sidestep issue #10 caused by DjangoZoom's deployment script executing the collectstatic command before creating the database structure with syncdb.  Thanks to Joost Cassee (https://github.com/jcassee) for reporting this one.
* Perform extra validation of the image cache directory and fallback to creating a temporary directory on validation failure
* Fixed a source creation bug, that caused invalid links to a non existing source transformation to appear on the sidebar


Version 0.8.2
-------------
* Moved code to Django 1.3

  - Users have to use the ``collectstatic`` management command::

    $ ./manage.py collectstatic

  - The ``site_media`` directory is no more, users must update the media
    serving directives in current deployments and point them to the
    ``static`` directory instead
    
* The changelog is now available under the ``about`` main menu
* ``Grappelli`` no longer bundled with Mayan

  - Users must install Grappelli or execute::
  
    $ pip install --upgrade -r requirements/production.txt

* Even easier UI language switching
* Added email login method, to enable it, set::
  
    AUTHENTICATION_BACKENDS = ('common.auth.email_auth_backend.EmailAuthBackend',)
    COMMON_LOGIN_METHOD = 'email'


Version 0.8.1
-------------
* Tags can now also be created from the main menu
* Added item count column to index instance list view
* Updated document indexing widget to show different icon for indexes or
  indexes that contain documents
* Replaced the Textarea widget with the TextAreaDiv widget on document
  and document page detail views

  - This change will allow highlighting search terms in the future
  
* Unknown document file format page count now defaults to 1

  - When uploading documents which the selected converted backend doesn't
    understand, the total page count will fallback to 1 page to at least
    show some data, and a comment will be automatically added to the 
    document description
    
* Added new MAIN_DISABLE_ICONS to turn off all icons

  - This options works very well when using the ``default`` theme
  
* The default theme is now ``activo``
* Improved document page views and document page transformation views
  navigation
* Added OCR queue document transformations

  - Use this for doing resizing or rotation fixes to improve OCR results
  
* Added reset view link to the document page view to reset the zoom 
  level and page rotation
* Staging files now show a thumbnail preview instead of preview link


Version 0.8.0
-------------
* Distributed OCR queue processing via celery is disabled for the time
  being
* Added support for local scheduling of jobs

  - This addition removes celery beat requirement, and make is optional
  
* Improve link highlighting
* Navigation improvements
* Documents with an unknown file format now display a mime type place
  holder icon instead of a error icon
* Mayan now does pre caching of document visual representation improving
  overall thumbnail, preview and display speed
  
  - Page image rotation and zooming is faster too with this update
  
* Removed all QUALITY related settings
* ``COMMON_TEMPORARY_DIRECTORY`` is now validated when Mayan starts and if
  not valid falls back to creating it's own temporary folder
* Added PDF file support to the python converter backend via ghostscript

  - This requires the installation of:
    
    + ghostscript python package
    + ghostscript system binaries and libraries
        
* Added PDF text parsing support to the python converter backend

  - This requires the installation of:
    
    + pdfminer python package
        
* Added PDF page count support to the python converter backend
* Added python only converter backend supporting resizing, zooming and rotation

  - This backend required the installation of the python image library (PIL)
  - This backend is useful when Graphicsmagick or Imagemagick can not be installed for some reason
  - If understand fewer file format than the other 2 backends
    
* Added default tranformation support to document sources
* Removed ``DOCUMENT_DEFAULT_TRANSFORMATIONS`` setup options
* Document sources are now defined via a series of view under the setup main menu
* This removes all the ``DOCUMENT_STAGING`` related setup options
  
  - Two document source types are supported local (via a web form), 
    and staging
  - However multiple document sources can be defined each with their own
    set of transformations and default metadata selection
      
* Use ``python-magic`` to determine a document's mimetype otherwise 
  fallback to use python's mimetypes library
* Remove the included sources for ``python-magic`` instead it is now fetched
  from github by pip
* Removed the document subtemplates and changed to a tabbed style
* Added link to document index content view to navigate the tree upwards
* Added new option ``MAIN_DISABLE_HOME_VIEW`` to disable the home main menu
  tab and save some space
* Added new option to the web theme app, ``WEB_THEME_VERBOSE_LOGIN``
  that display a more information on the login screen
  (version, copyright, logos)
* Added a confirmation dialog to the document tag removal view

Version 0.7.6
-------------
* Added recent searches per user support

  - The ammount of searches stored is controlled by the setup option
    ``SEARCH_RECENT_COUNT``
      
* The document page zoom button are now disabled when reaching the minimum
  or maximum zoom level
* The document page navigation links are now disabled when view the first
  and last page of a document
* Document page title now displays the current page vs the total page
  count
* Document page title now displays the current zoom level and rotation
  degrees
* Added means set the expansion compressed files during document creation,
  via web interface removing the need for the configuration options:
  ``UNCOMPRESS_COMPRESSED_LOCAL_FILES`` and ``UNCOMPRESS_COMPRESSED_STAGING_FILES``
* Added 'search again' button to the advances search results view
* Implementes an advanced search feature, which allows for individual field terms

  - Search fields supported: document type, MIME type, filename, 
    extension, metadata values, content, description, tags, comments

Version 0.7.5
-------------
* Added a help messages to the sidebar of some views
* Renamed some forms submit button to more intuitive one

  - 'Search' on the submit button of the search form
  - 'Next step' on the document creation wizard
  
* Added view to list supported file formats and reported by the
  converter backend
* Added redirection support to multi object action views
* Renamed 'document list' link to 'all documents' and
  'recent document list' to 'recent documents'
* Removed 'change password' link next to the current user's name and
  added a few views to handle the current user's password, details and
  details editing
  
Version 0.7.4
-------------
* Renamed 'secondary actions' to 'secondary menu' 
* Added document type setup views to the setup menu
* Added document type file name editing views to the setup menu
* Fixed document queue properties sidebar template not showing

Version 0.7.3
-------------
* Refactored main menu navigation and converted all apps to this new
  system
* Multi item links are now displayed on top of generic lists as well as
  on the bottom
* Spanish translation updates
* Updated requirements to use the latest development version of
  django-mptt
* Improved user folder document removal views
* Added ability to specify default metadata or metadataset per
  document type
* Converted filename handling to use os.path library for improved 
  portability
* Added edit source object attribute difference detection and logging
  to history app
* Missing metadata type in a document during a multi document editing doesn't raise errors anymore.

  - This allows for multi document heterogeneous metadata editing in a single step.
    
* Added document multi item links in search results

  - Direct editing can be done from the search result list
    
* Permissions are now grouped and assigned a group name
* Improved role management views
* Document type is now an optional document property

  - Documents can be created without an explicit document type
    
* Added support for per user staging directories
* Updated logos

Version 0.7
-----------
* Added confirmation dialogs icons
* Added comment app with support for adding and deleting comments to 
  and from documents
* Updated requirements files as per issue #9
* Show tagged item count in the tag list view
* Show tagget document link in the tags subtemplate of documents
* Made comment sorted by oldest first, made comment subtemplate
  scrollable
* Rename comments app to document_comment to avoid conflict with 
  Django's comment app
* Made document comments searchable

Version 0.5.1
-------------
* Applied initial merge of the new subtemplate renderer
* Fixed tag removal logic
* Initial commit to support document comments
* Updated so that loading spinner is displayed always
* Exclude tags from the local document upload form
* Added document tagging support

  - Requires installing ``django-taggit`` and doing a ``sync-db``

Version 0.5
-----------
* Added tag list view and global tag delete support
* Added tag editing view and listing documents with an specific tag
* Changed the previewing and deleting staging files views to required
  ``DOCUMENT_CREATE`` permission
* Added no-parent-history class to document page links so that iframe clicking doesn't affect the parent window history

  - Fixes back button issue on Chrome 9 & 10
  
* Added per app version display tag
* Added loading spinner animation
* Messages tweaks and translation updates
* Converter app cleanups, document pre-cache, magic number removal
* Added OCR view displaying all active OCR tasks from all cluster nodes
* Disabled ``CELERY_DISABLE_RATE_LIMITS`` by default
* Implement local task locking using Django locmem cache backend
* Added doc extension to office document format list
* Removed redundant transformation calculation
* Make sure OCR in processing documents cannot be deleted
* PEP8, pylint cleanups and removal of relative imports
* Removed the obsolete ``DOCUMENTS_GROUP_MAX_RESULTS`` setting option
* Improved visual appearance of messages by displaying them outside the
  main form
* Added link to close all notifications with one click
* Made the queue processing interval configurable by means of a new
  setting: ``OCR_QUEUE_PROCESSING_INTERVAL``
* Added detection and reset of orphaned ocr documents being left as
  'processing' when celery dies
* Improved unknown format detection in the graphicsmagick backend
* Improved document convertion API
* Added initial support for converting office documents (only ods and
  docx tested)
* Added sample configuration files for supervisor and apache under
  contrib/
* Avoid duplicates in recent document list
* Added the configuration option CONVERTER_GM_SETTINGS to pass
  GraphicsMagicks specific commands the the GM backend
* Lower image convertion quality if the format is jpg
* Inverted the rotation button, more intuitive this way
* Merged and reduced the document page zoom and rotation views
* Increased permissions app permission's label field size

  - DB Update required
    
* Added support for metadata group actions
* Reduced the document pages widget size
* Display the metadata group numeric total in the metadata group form
  title
* Reorganized page detail icons
* Added first & last page navigation links to document page view
* Added interactive zoom support to document page detail view
* Spanish translation updates
* Added ``DOCUMENTS_ZOOM_PERCENT_STEP``, ``DOCUMENTS_ZOOM_MAX_LEVEL``,
  ``DOCUMENTS_ZOOM_MIN_LEVEL`` configuration options to allow detailed
  zoom control
* Added interactive document page view rotation support
* Changed the side bar document grouping with carousel style document
  grouping form widget
* Removed the obsolete ``DOCUMENTS_TRANFORMATION_PREVIEW_SIZE`` and
  ``DOCUMENTS_GROUP_SHOW_THUMBNAIL`` setting options
* Improved double submit prevention
* Added a direct rename field to the local update and staging upload
  forms
* Separated document page detail view into document text and document
  image views
* Added grab-scroll to document page view
* Disabled submit buttons and any buttons when during a form submit
* Updated the page preview widget to display a infinite-style horizontal
  carousel of page previews
* Added support user document folders

  - Must do a ``syncdb`` to add the new tables
    
* Added support for listing the most recent accessed documents per user
* Added document page navigation
* Fixed diagnostics url resolution
* Added confirmation dialog to document's find missing document file
  diagnostic
* Added a document page edit view
* Added support for the command line program pdftotext from the
  poppler-utils packages to extract text from PDF documents without
  doing OCR
* Fixed document description editing
* Replaced page break text with page number when displaying document
  content
* Implemented detail form readonly fields the correct way, this fixes
  copy & paste issues with Firefox
* New document page view
* Added view to add or remove user to a specific role
* Updated the jQuery packages with the web_theme app to version 1.5.2
* Made ``AVAILABLE_INDEXING_FUNCTION`` setting a setting of the documents 
  app instead of the filesystem_serving app
* Fixed document download in FireFox for documents containing spaces in
  the filename
* If mime detection fails set mime type to '' instead of 'unknown'
* Use document MIME type when downloading otherwise use
  'application/octet-stream' if none
* Changed the way document page count is parsed from the graphics
  backend, fixing issue #7
* Optimized document metadata query and display
* Implemented OCR output cleanups for English and Spanish
* Redirect user to the website entry point if already logged and lands
  in the login template
* Changed from using SimpleUploadedFile class to stream file to the
  simpler File class wrapper
* Updated staging files previews to use sendfile instead of serve_file
* Moved staging file preview creation logic from documents.views to
  staging.py
* When deleting staging file, it's cached preview is also deleted
* Added a new setup option:

  - ``FILESYSTEM_INDEXING_AVAILABLE_FUNCTIONS`` - a dictionary to allow users
    to add custom functions
      
* Made automatic OCR a function of the OCR app and not of Documents app (via signals)

  - Renamed setup option ``DOCUMENT_AUTOMATIC_OCR`` to ``OCR_AUTOMATIC_OCR``
    
* Clear node name when requeueing a document for OCR
* Added support for editing the metadata of multiple documents at the
  same time
* Added Graphics magick support by means of user selectable graphic convertion backends

  - Some settings renamed to support this change:
    
    + ``CONVERTER_CONVERT_PATH`` is now ``CONVERTER_IM_CONVERT_PATH``
    + ``CONVERTER_IDENTIFY_PATH`` is now ``CONVERTER_IM_IDENTIFY_PATH``
        
  - Added options:
    
    + ``CONVERTER_GM_PATH`` - File path to graphicsmagick's program.
    + ``CONVERTER_GRAPHICS_BACKEND`` - Backend to use: ``ImageMagick`` or 
      ``GraphicMagick``
          
* Raise ImportError and notify user when specifying a non existant
  converter graphics backend
* Fixed issue #4, avoid circular import in permissions/__init__.py
* Add a user to a default role only when the user is created
* Added total page count to statistics view
* Added support to disable the default scrolling JS code included in
  web_theme app, saving some KBs in transfer
* Clear last ocr results when requeueing a document
* Removed the 'exists' column in document list view, diagnostics
  superceded this
* Added 3rd party sendfile app (support apache's X-sendfile)
* Updated the get_document_image view to use the new sendfile app
* Fixed the issue of the strip spaces middleware conflicting with
  downloads
* Removed custom IE9 tags
* Closed Issue #6
* Allow deletion of non existing documents from OCR queue
* Allow OCR requeue of pending documents
* Invalid page numbers now raise Http404, not found instead of error
* Added an additional check to lower the chance of OCR race conditions
  between nodes
* Introduce a random delay to each node to further reduce the chance of
  a race condition, until row locking can be implemented or is
  implemented by Django
* Moved navigation code to its own app
* Reimplemented OCR delay code, only delay new document
  Added a new field: delay, update your database schema accordingly
* Made the concurrent ocr code more granular, per node, every node can
  handle different amounts of concurrent ocr tasks
  Added a new field: node_name, update your database schema acordinging
* Reduced default ocr delay time
* Added a new diagnostics tab under the tools menu
* Added a new option ``OCR_REPLICATION_DELAY`` to allow the storage some
  time for replication before attempting to do OCR to a document
* Added OCR multi document re-queue and delete support
* Added simple statistics page (total used storage, total docs, etc)
* Implemented form based and button based multi item actions (button
  based by default)
* Added multi document delete
* Fixed a few HTML validation errors
* Issues are now tracked using github
* Added indexing flags to ocr model
* Small optimization in document list view
* Small search optimization
* Display "DEBUG mode" string in title if ``DEBUG`` variable is set to True
* Added the fix-permissions bash script under misc/ folder
* Plugged another file descriptor leak
* Show class name in config settings view
* Added missing config option from the setup menu
* Close file descriptor to avoid leaks
* Don't allow duplicate documents in queues
* Don't raise ``PermissionDenied`` exception in ``PermissionDenied middleware``,
  even while debugging
* Fixed page number detection
* Created 'simple document' for non technical users with all of a
  document pages content
* Use document preview code for staging file also
* Error picture literal name removal
* Spanish translation updates
* Show document file path in regards of its storage
* Added new setting: side bar search box
* Implemented new ``PermissioDenied`` exception middleware handler
* Permissions app api now returns a ``PermissionDenied`` exception instead
  of a custom one
* Added new 403 error template
* Updated the 404 template to display only a not found message
* Moved the login required middleware to the common app
* Fixed search app's model.objects.filter indentation, improved result
  count calculation
* Added dynamic comparison types to search app
* Separated search code from view code
* Correctly calculate show result count for multi model searches
* Fixed OCR queue list showing wrong thumbnail
* Fixed staging file preview
* Show current metadata in document upload view sidebar
* Show sentry login for admin users
* Do not reinitialize document queue and/or queued document on reentry
* Try extra hard not to assign same uuid to two documents
* Added new transformation preview size setting
* Renamed document queue state links
* Changed ocr status display sidebar from form based to text based
* Added document action to clear all the document's page transformations
* Allow search across related fields
* Optimzed search for speed and memory footprint
* Added ``LIMIT`` setting to search
* Show search elapsed time on result page
* Converter now differentiates between unknown file format and convert
  errors 
* Close file descriptors when executing external programs to
  prevent/reduce file descriptior leaks
* Improved exception handling of external programs
* Show document thumbnail in document ocr queue list
* Make ocr document date submitted column non breakable
* Fix permissions, directories set to mode 755 and files to mode 644
* Try to fix issue #2, "random ORM field error on search while doing OCR"
* Added configurable location setting for file based storage
* Prepend storage name to differentiate config options
* Fixed duplicated document search
* Optimized document duplicate search
* Added locale middleware, menu bar language switching works now
* Only show language selection list if localemiddleware is active
* Spanish translation updates
* Added links, views and permissions to disable or enable an OCR queue
* Enabled Django's template caching
* Added document queue property side bar window to the document queue
  list view
* Added HTML spaceless middleware to remove whitespace in HTML code
* If current user is superuser or staff show thumbnail & preview
  generation error messages
* Added a setting to show document thumbnail in metadata group list
* Started adding configurations setting descriptions
* Initial GridFS storage support
* Implemented size and delete methods for GridFS
* Implement GridFS storage user settings
* Added document link in the OCR document queue list
* Link to manually re queue failed OCR
* Don't separate links (encose object list links with white-space:
  nowrap;)
* Added document description to the field search list
* Sort OCR queued documents according to submitted date & time
* Document filesystem serving is now a separate app

  - Steps to update (Some warnings may be returned, but these are not
    fatal as they might be related to missing metadata in some documents):
  
    + rename the following settings:
    
      + ``DOCUMENTS_FILESYSTEM_FILESERVING_ENABLE`` to ``FILESYSTEM_FILESERVING_ENABLE``
      + ``DOCUMENTS_FILESYSTEM_FILESERVING_PATH`` to ``FILESYSTEM_FILESERVING_PATH``
      + ``DOCUMENTS_FILESYSTEM_SLUGIFY_PATHS`` to ``FILESYSTEM_SLUGIFY_PATHS``
      + ``DOCUMENTS_FILESYSTEM_MAX_RENAME_COUNT`` to ``FILESYSTEM_MAX_RENAME_COUNT``
      
    + Do a ./manage.py syncdb
    + Execute 'Recreate index links' locate in the tools menu
    + Wait a few minutes
      
* Added per document duplicate search and a tools menu option to seach
  all duplicated documents
* Added document tool that deletes and re-creates all documents
  filesystem links
* Increased document's and document metadata index filename field's size
  to 255 characters
* Added sentry to monitor and store error for later debugging
* Zip files can now be uncompressed in memory and their content uploaded
  individually in one step
* Added support for concurrent, queued OCR processing using celery
* Apply default transformations to document before OCR
* Added unpaper to the OCR convertion pipe
* Added views to create, edit and grant/revoke permissions to roles
* Added multipage documents support (only tested on pdfs)

  - To update a previous database do: [d.update_page_count() for d in Document.objects.all()]
    
* Added support for document page transformation (no GUI yet)
* Added permissions and roles support
* Added python-magic for smarter MIME type detection
  (https://github.com/ahupp/python-magic).
* Added a new Document model field: file_mime_encoding.
* Show only document metadata in document list view.
* If one document type exists, the create document wizard skips the
  first step.
* Changed to a liquid css grid
* Added the ability to group documents by their metadata
* New abstracted options to adjust document conversion quality (default,
  low, high)
