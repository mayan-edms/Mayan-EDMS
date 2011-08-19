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
    

    
