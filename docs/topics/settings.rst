========
Settings
========

**Mayan EDMS** has many configuration options that make it very adaptable to
different server configurations.

Documents
=========

.. setting:: DOCUMENTS_CHECKSUM_FUNCTION

**DOCUMENTS_CHECKSUM_FUNCTION**

Default: ``hashlib.sha256(x).hexdigest()``

The function that will be used to calculate the hash value of each uploaded document.


.. setting:: DOCUMENTS_UUID_FUNCTION

**DOCUMENTS_UUID_FUNCTION**

Default: ``unicode(uuid.uuid4())``

The function that will be used to internally identify each uploaded document.


.. setting:: DOCUMENTS_STORAGE_BACKEND

**DOCUMENTS_STORAGE_BACKEND**

Default: ``FileBasedStorage`` class

The storage backend that will be used to store every document.


.. setting:: DOCUMENTS_PREVIEW_SIZE

**DOCUMENTS_PREVIEW_SIZE**
    
Default: ``640x480``

Size of the document list and recent document list previews.


.. setting:: DOCUMENTS_PRINT_SIZE

**DOCUMENTS_PRINT_SIZE**
    
Default: ``1400``
    

.. setting:: DOCUMENTS_MULTIPAGE_PREVIEW_SIZE    

**DOCUMENTS_MULTIPAGE_PREVIEW_SIZE**

Default: ``160x120``


.. setting:: DOCUMENTS_THUMBNAIL_SIZE

**DOCUMENTS_THUMBNAIL_SIZE**
    
Default: ``50x50``
        

.. setting:: DOCUMENTS_DISPLAY_SIZE    

**DOCUMENTS_DISPLAY_SIZE**
    
Default: ``1200``
          

.. setting:: DOCUMENTS_RECENT_COUNT

**DOCUMENTS_RECENT_COUNT**
    
Default: ``40``  
    
Maximum number of recent (created, edited, viewed) documents to
remember per user.   
    

.. setting:: DOCUMENTS_ZOOM_PERCENT_STEP

**DOCUMENTS_ZOOM_PERCENT_STEP**
    
Default: ``50``  
    
Amount in percent zoom in or out a document page per user interaction.    
    
    
.. setting:: DOCUMENTS_ZOOM_MAX_LEVEL    

**DOCUMENTS_ZOOM_MAX_LEVEL**
    
Default: ``200``  
    
Maximum amount in percent (%) to allow user to zoom in a document page interactively.

    
.. setting:: DOCUMENTS_ZOOM_MIN_LEVEL

**DOCUMENTS_ZOOM_MIN_LEVEL**
    
Default: ``50``  
    
Minimum amount in percent (%) to allow user to zoom out a document page interactively.
    

.. setting:: DOCUMENTS_ROTATION_STEP

**DOCUMENTS_ROTATION_STEP**
    
Default: ``90``  
    
Amount in degrees to rotate a document page per user interaction.    
    
    
.. setting:: DOCUMENTS_CACHE_PATH

**DOCUMENTS_CACHE_PATH**
    
Default: ``image_cache`` (relative to the installation path)
    
The path where the visual representations of the documents are stored for fast display.
    

Converter
=========
.. setting:: CONVERTER_GRAPHICS_BACKEND

**CONVERTER_GRAPHICS_BACKEND**

Default: ``converter.backends.python``    
    
Graphics conversion backend to use. Options are:

* ``converter.backends.imagemagick`` - Wrapper for ImageMagick

  * Use the :setting:`CONVERTER_IM_CONVERT_PATH` and :setting:`CONVERTER_IM_IDENTIFY_PATH` to specify the binary files locations.
  
* ``converter.backends.graphicsmagick`` - Wrapper for GraphicsMagick

  * Use the :setting:`CONVERTER_GM_PATH` and :setting:`CONVERTER_GM_SETTINGS` to specify the binary file location and customized settings.

* ``converter.backends.python`` - Wrapper for Pillow_ and Ghostscript_


.. _Pillow: http://pypi.python.org/pypi/Pillow
.. _Ghostscript: http://www.ghostscript.com/


.. setting:: CONVERTER_IM_CONVERT_PATH

**CONVERTER_IM_CONVERT_PATH**
    
Default: ``/usr/bin/convert``
    
File path to imagemagick's convert program.    
    
    
.. setting:: CONVERTER_IM_IDENTIFY_PATH    
    
**CONVERTER_IM_IDENTIFY_PATH**

Default: ``/usr/bin/identify``

File path to imagemagick's identify program.    
    
    
.. setting:: CONVERTER_GM_PATH    

**CONVERTER_GM_PATH**

Default: ``/usr/bin/gm``
    
File path to graphicsmagick's program.
    

.. setting:: CONVERTER_GM_SETTINGS

**CONVERTER_GM_SETTINGS**

Default: None
   
Suggested options: ``-limit files 1 -limit memory 1GB -limit map 2GB -density 200``

Set of configuration options to pass to the GraphicsMagick executable to
fine tune it's functionality as explained in the `GraphicsMagick documentation`_

.. _GraphicsMagick documentation: http://www.graphicsmagick.org/convert.html#conv-opti


.. setting:: CONVERTER_LIBREOFFICE_PATH


**CONVERTER_LIBREOFFICE_PATH**

Default: ``/usr/bin/libreoffice``

Path to the libreoffice binary used to call LibreOffice for office document conversion.
    

   
Linking
=======

.. setting:: LINKING_SHOW_EMPTY_SMART_LINKS

**LINKING_SHOW_EMPTY_SMART_LINKS**
    
Default: ``True``
    
Show smart links even when they don't return any documents.
    

Storage
=======

.. setting:: STORAGE_GRIDFS_HOST

**STORAGE_GRIDFS_HOST**
    
Default: ``localhost``    
    

.. setting:: STORAGE_GRIDFS_PORT

**STORAGE_GRIDFS_PORT**
    
Default: ``27017``        
    
    
.. setting:: STORAGE_GRIDFS_DATABASE_NAME

**STORAGE_GRIDFS_DATABASE_NAME**
    
Default: ``document_storage``     
    
    
.. setting:: STORAGE_FILESTORAGE_LOCATION

**STORAGE_FILESTORAGE_LOCATION**
    
Default: ``document_storage``     
    

Document indexing
=================

.. setting:: DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS

**DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS**
    
Default: ``proper_name`` 


.. setting:: DOCUMENT_INDEXING_SUFFIX_SEPARATOR

**DOCUMENT_INDEXING_SUFFIX_SEPARATOR**
    
Default: ``_``  (underscore)

    
.. setting:: DOCUMENT_INDEXING_FILESYSTEM_SLUGIFY_PATHS

**DOCUMENT_INDEXING_FILESYSTEM_SLUGIFY_PATHS**
    
Default: ``False``    
        
    
.. setting:: DOCUMENT_INDEXING_FILESYSTEM_MAX_SUFFIX_COUNT

**DOCUMENT_INDEXING_FILESYSTEM_MAX_SUFFIX_COUNT**
    
Default: ``1000``        
    
    
.. setting:: DOCUMENT_INDEXING_FILESYSTEM_SERVING

**DOCUMENT_INDEXING_FILESYSTEM_SERVING**

Default: ``{}``

A dictionary that maps the index name and where on the filesystem that index will be mirrored.

    
OCR
===
    
.. setting:: OCR_TESSERACT_PATH

**OCR_TESSERACT_PATH**
    
Default: ``/bin/tesseract``        

File path to the ``tesseract`` executable, used to perform OCR on document
page's images.
    
    
.. setting:: OCR_TESSERACT_LANGUAGE

**OCR_TESSERACT_LANGUAGE**
    
Default: ``eng``           

Language code passed to the ``tesseract`` executable.
        
    
.. setting:: OCR_REPLICATION_DELAY

**OCR_REPLICATION_DELAY**
    
Default: ``0``              
    
Amount of seconds to delay OCR of documents to allow for the node's
storage replication overhead.    
    
    
.. setting:: OCR_NODE_CONCURRENT_EXECUTION

**OCR_NODE_CONCURRENT_EXECUTION**
    
Default: ``1``               
    
Maximum amount of concurrent document OCRs a node can perform.


.. setting:: OCR_AUTOMATIC_OCR

**OCR_AUTOMATIC_OCR**
    
Default: ``True``               
    
Automatically queue newly created documents or newly uploaded versions
of existing documents for OCR.
    
    
.. setting:: OCR_QUEUE_PROCESSING_INTERVAL

**OCR_QUEUE_PROCESSING_INTERVAL**
    
Default: ``10``               


.. setting:: OCR_UNPAPER_PATH

**OCR_UNPAPER_PATH**
    
Default: ``/usr/bin/unpaper`` 
    
File path to the ``unpaper`` executable, used to clean up images before
doing OCR.

    
.. setting:: OCR_PDFTOTEXT_PATH

**OCR_PDFTOTEXT_PATH**
    
Default: ``/usr/bin/pdftotext`` 
    
File path to ``poppler's`` ``pdftotext`` program used to extract text
from PDF files.


Metadata
========

.. setting:: METADATA_AVAILABLE_FUNCTIONS

**METADATA_AVAILABLE_FUNCTIONS**

Default: ``current_date`` 


.. setting:: METADATA_AVAILABLE_MODELS

**METADATA_AVAILABLE_MODELS**

Default: ``User`` 


Common
======

.. setting:: COMMON_TEMPORARY_DIRECTORY

**COMMON_TEMPORARY_DIRECTORY**

Default: ``/tmp`` 

Temporary directory used site wide to store thumbnails, previews
and temporary files. If none is specified, one will be created 
using tempfile.mkdtemp()


.. setting:: COMMON_DEFAULT_PAPER_SIZE

**COMMON_DEFAULT_PAPER_SIZE**

Default: ``Letter`` 


.. setting:: COMMON_DEFAULT_PAGE_ORIENTATION

**COMMON_DEFAULT_PAGE_ORIENTATION**

Default: ``Portrait`` 


.. setting:: COMMON_AUTO_CREATE_ADMIN

**COMMON_AUTO_CREATE_ADMIN**

Default: ``True`` 

Automatically creates an administrator superuser with the username
specified by COMMON_AUTO_ADMIN_USERNAME and with the default password
specified by COMMON_AUTO_ADMIN_PASSWORD


.. setting:: COMMON_AUTO_ADMIN_USERNAME

**COMMON_AUTO_ADMIN_USERNAME**

Default: ``admin`` 

Username of the automatically created superuser


.. setting:: COMMON_AUTO_ADMIN_PASSWORD

**COMMON_AUTO_ADMIN_PASSWORD**

Default: Random generated password

The password of the automatically created superuser
    

.. setting:: COMMON_LOGIN_METHOD

**COMMON_LOGIN_METHOD**

Default: ``username`` 

Controls the mechanism used to authenticated user. Options are: ``username``, ``email``
If using the ``email`` login method a proper email authentication backend must used
such as AUTHENTICATION_BACKENDS = ('common.auth.email_auth_backend.EmailAuthBackend',)


.. setting:: COMMON_ALLOW_ANONYMOUS_ACCESS

**COMMON_ALLOW_ANONYMOUS_ACCESS**

Default: ``False``

Allow non authenticated users, access to all views.


Search
======

.. setting:: SEARCH_LIMIT 

**SEARCH_LIMIT**

Default: ``100`` 

Maximum amount search hits to fetch and display.


.. setting:: SEARCH_RECENT_COUNT

**SEARCH_RECENT_COUNT**

Default: ``5`` 

Maximum number of search queries to remember per user.    


Web theme
=========

.. setting:: WEB_THEME_THEME

**WEB_THEME_THEME**

Default: ``activo`` 

CSS theme to apply, options are: ``amro``, ``bec``, ``bec-green``, ``blue``,
``default``, ``djime-cerulean``, ``drastic-dark``, ``kathleene``, ``olive``,
``orange``, ``red``, ``reidb-greenish`` and ``warehouse``.


.. setting:: WEB_THEME_VERBOSE_LOGIN

**WEB_THEME_VERBOSE_LOGIN**

Default: ``True`` 

Display extra information in the login screen.


Main
====

.. setting:: MAIN_SIDE_BAR_SEARCH

**MAIN_SIDE_BAR_SEARCH**

Default: ``False`` 

Controls whether the search functionality is provided by a sidebar widget or by a menu entry.


.. setting:: MAIN_DISABLE_HOME_VIEW

**MAIN_DISABLE_HOME_VIEW**

Default: ``False`` 

Disable the home view and redirect users straight to the recent document list as soon as they log in.


.. setting:: MAIN_DISABLE_ICONS

**MAIN_DISABLE_ICONS**

Default: ``False`` 

Turns off navigation links' icons.


User management
===============

.. setting:: ROLES_DEFAULT_ROLES

**ROLES_DEFAULT_ROLES**

Default: ``[]`` 

A list of existing roles that are automatically assigned to newly created users


Signatures
==========

.. setting:: SIGNATURES_KEYSERVERS    

**SIGNATURES_KEYSERVERS**

Default: ``['pool.sks-keyservers.net']`` 

List of keyservers to be queried for unknown keys.


.. setting:: SIGNATURES_GPG_HOME

**SIGNATURES_GPG_HOME**

Default: ``gpg_home``

Home directory used to store keys as well as configuration files.
