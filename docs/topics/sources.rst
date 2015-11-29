=======
Sources
=======

Document sources define places from which documents can be uploaded or gathered.

The current document sources supported are:

- Web - ``HTML`` forms with a ``Browse`` button that will open the file dialog
  when clicked to allow selection of files in the user's computer to be
  uploaded as documents.
- Staging folder - Folder where networked attached scanned can save image
  files. The files in these staging folders are scanned and a preview is
  generated to help the process of upload.
- POP3 email - Provide the email, server and credential of a ``POP3`` based
  email to be scanned periodically for email. The body of the email is uploaded
  as a document and the attachments of the email are uploaded as separate
  documents.
- IMAP email - Same as the ``POP3`` email source but for email accounts using
  the ``IMAP`` protocol.
- Watch folder - A filesystem folder that is scanned periodically for files.
  Any file in the watch folder is automatically uploaded.

Document source can be configure to allow document bundles to uploaded as
compressed files which are decompressed and their content uploaded as separate
documents. This feature is useful when migrating from another document
manager system.
