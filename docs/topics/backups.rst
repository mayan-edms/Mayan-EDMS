=======
Backups
=======

To backup your install of Mayan EDMS just copy the actual document files and
the database content. If you are using the default storage backend, the
document files should be found in ``mayan/media/document_storage/``.

To dump the content of your database manager refer to the documentation chapter
regarding database data "dumping".

Example:

 - Postgresl: http://www.postgresql.org/docs/current/static/backup.html
 - MySQL: https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html
 - SQLite: Just copy the file ``mayan/media/db.sqlite3``
