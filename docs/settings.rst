========
Settings
========

Mayan EDMS has many configuration options that make it very adaptable to
different server configurations.

Documents
---------

.. data:: DOCUMENTS_CHECKSUM_FUNCTION

    Default: ``hashlib.sha256(x).hexdigest()``


.. data:: DOCUMENTS_UUID_FUNCTION

    Default: ``unicode(uuid.uuid4())``


.. data:: DOCUMENTS_STORAGE_BACKEND

    Default: ``FileBasedStorage`` class


.. data:: DOCUMENTS_PREVIEW_SIZE    
    
    Default: ``640x480``


.. data:: DOCUMENTS_PRINT_SIZE    
    
    Default: ``1400``
    

.. data:: DOCUMENTS_MULTIPAGE_PREVIEW_SIZE    
    
    Default: ``160x120``


.. data:: DOCUMENTS_THUMBNAIL_SIZE    
    
    Default: ``50x50``
        

.. data:: DOCUMENTS_DISPLAY_SIZE    
    
    Default: ``1200``
          

.. data:: DOCUMENTS_RECENT_COUNT    
    
    Default: ``40``  
    
    Maximum number of recent (created, edited, viewed) documents to
    remember per user.   
    

.. data:: DOCUMENTS_ZOOM_PERCENT_STEP    
    
    Default: ``50``  
    
    Amount in percent zoom in or out a document page per user interaction.    
    
    
.. data:: DOCUMENTS_ZOOM_MAX_LEVEL    
    
    Default: ``200``  
    
    Maximum amount in percent (%) to allow user to zoom in a document page interactively.

    
.. data:: DOCUMENTS_ZOOM_MIN_LEVEL    
    
    Default: ``50``  
    
    Minimum amount in percent (%) to allow user to zoom out a document page interactively.
    

.. data:: DOCUMENTS_ROTATION_STEP    
    
    Default: ``90``  
    
    Amount in degrees to rotate a document page per user interaction.    
    
    
.. data:: DOCUMENTS_CACHE_PATH    
    
    Default: ``image_cache`` (relative to the installation path)
    

Converter
---------
    
.. data:: CONVERTER_IM_CONVERT_PATH    
    
    Default: ``/usr/bin/convert``
    
    
    File path to imagemagick's convert program.    
    
    
.. data:: CONVERTER_IM_IDENTIFY_PATH    
    
    Default: ``/usr/bin/identify``
    
    
    File path to imagemagick's identify program.    
    
    
.. data:: CONVERTER_GM_PATH    
    
    Default: ``/usr/bin/gm``
    
    
    File path to graphicsmagick's program.
    

.. data:: CONVERTER_GM_SETTINGS    
    
    Default: None
    
    
.. data:: CONVERTER_GRAPHICS_BACKEND    
    
    Default: ``converter.backends.python``    
    
    Graphics conversion backend to use. Options are: ``converter.backends.imagemagick``,
    ``converter.backends.graphicsmagick`` and ``converter.backends.python``.
    
    
.. data:: CONVERTER_UNOCONV_PATH    
    
    Default: ``/usr/bin/unoconv``
    
    
Groupping
---------

.. data:: GROUPING_SHOW_EMPTY_GROUPS    
    
    Default: ``True``
    

Storage
-------

.. data:: STORAGE_GRIDFS_HOST    
    
    Default: ``localhost``    
    

.. data:: STORAGE_GRIDFS_PORT    
    
    Default: ``27017``        
    
    
.. data:: STORAGE_GRIDFS_DATABASE_NAME    
    
    Default: ``document_storage``     
    
    
.. data:: STORAGE_FILESTORAGE_LOCATION    
    
    Default: ``document_storage``     
    
    
Job processor
-------------
    
.. data:: JOB_PROCESSING_BACKEND    
    
    Default: ``None``  
    
    
    Specified which job processing library to use, option are: None and celery.


Document indexing
-----------------

.. data:: DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS    
    
    Default: ``proper_name`` 


.. data:: DOCUMENT_INDEXING_SUFFIX_SEPARATOR    
    
    Default: ``_``  (underscore)
    
    
.. data:: DOCUMENT_INDEXING_FILESYSTEM_SLUGIFY_PATHS    
    
    Default: ``False``    
        
    
.. data:: DOCUMENT_INDEXING_FILESYSTEM_MAX_SUFFIX_COUNT    
    
    Default: ``1000``        
    
    
.. data:: DOCUMENT_INDEXING_FILESYSTEM_FILESERVING_PATH    
    
    Default: ``/tmp/mayan/documents``         
    
    
.. data:: DOCUMENT_INDEXING_FILESYSTEM_FILESERVING_ENABLE    
    
    Default: ``True``       
    
    
OCR
---
    
.. data:: OCR_TESSERACT_PATH    
    
    Default: ``/bin/tesseract``        
    
    
.. data:: OCR_TESSERACT_LANGUAGE    
    
    Default: ``eng``           
    
    
.. data:: OCR_REPLICATION_DELAY    
    
    Default: ``10``               
    
    Amount of seconds to delay OCR of documents to allow for the node's
    storage replication overhead.    
    
    
.. data:: OCR_NODE_CONCURRENT_EXECUTION    
    
    Default: ``1``               
    
    Maximum amount of concurrent document OCRs a node can perform.


.. data:: OCR_AUTOMATIC_OCR    
    
    Default: ``False``               
    
    Automatically queue newly created documents for OCR.
    
    
.. data:: OCR_QUEUE_PROCESSING_INTERVAL    
    
    Default: ``10``               


.. data:: OCR_CACHE_URI    
    
    Default: ``None``       

    URI in the form: ``"memcached://127.0.0.1:11211/"`` to specify a cache
    backend to use for locking. Multiple hosts can be specified separated
    by a semicolon.    
    

.. data:: OCR_UNPAPER_PATH    
    
    Default: ``/usr/bin/unpaper`` 
    
    File path to unpaper program.
    

Metadata
--------

.. data:: METADATA_AVAILABLE_FUNCTIONS    
    
    Default: ``current_date`` 
   
   
.. data:: METADATA_AVAILABLE_MODELS    
    
    Default: ``User`` 
   
   
Common
------
   
.. data:: COMMON_TEMPORARY_DIRECTORY    
    
    Default: ``/tmp`` 
    
    Temporary directory used site wide to store thumbnails, previews
    and temporary files. If none is specified, one will be created 
    using tempfile.mkdtemp()


.. data:: COMMON_DEFAULT_PAPER_SIZE    
    
    Default: ``Letter`` 
    

.. data:: COMMON_DEFAULT_PAGE_ORIENTATION    
    
    Default: ``Portrait`` 
    

.. data:: COMMON_AUTO_CREATE_ADMIN    
    
    Default: ``True`` 
    
    
.. data:: COMMON_AUTO_ADMIN_USERNAME    
    
    Default: ``admin`` 
    
    
.. data:: COMMON_AUTO_ADMIN_PASSWORD    
    
    Default: ``admin`` 
        
    
.. data:: COMMON_LOGIN_METHOD    
    
    Default: ``username`` 
    
    Controls the mechanism used to authenticated user. Options are: ``username``, ``email``    
    
    
Search
------

.. data:: SEARCH_LIMIT    
    
    Default: ``100`` 
    
    Maximum amount search hits to fetch and display.
    
    
.. data:: SEARCH_RECENT_COUNT    
    
    Default: ``5`` 
    
    Maximum number of search queries to remember per user.    
    

Web theme
---------

.. data:: WEB_THEME_THEME    
    
    Default: ``activo`` 
    
    CSS theme to apply, options are: ``amro``, ``bec``, ``bec-green``, ``blue``, ``default``, ``djime-cerulean``, ``drastic-dark``, ``kathleene``, ``olive``, ``orange``, ``red``, ``reidb-greenish`` and ``warehouse``.
    
    
.. data:: WEB_THEME_VERBOSE_LOGIN    
    
    Default: ``True`` 
    
    Display extra information in the login screen.
    
    
Main
----

.. data:: MAIN_SIDE_BAR_SEARCH    
    
    Default: ``False`` 
    
    Controls whether the search functionality is provided by a sidebar widget or by a menu entry.
    

.. data:: MAIN_DISABLE_HOME_VIEW    
    
    Default: ``False`` 


.. data:: MAIN_DISABLE_ICONS    
    
    Default: ``False`` 
    
    
User management
-----

.. data:: ROLES_DEFAULT_ROLES    
    
    Default: ``[]`` 
    
    A list of existing roles that are automatically assigned to newly created users
