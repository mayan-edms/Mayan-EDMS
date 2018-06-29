=======
Backups
=======

To backup your install of Mayan EDMS just copy the actual document files and
the database content. If you are using the default storage backend, the
document files should be found in the ``media`` folder of your installation.

To dump the content of your database manager refer to the documentation chapter
regarding database data "dumping".

Here is an example of how to perform a backup and a restore of a PostgreSQL
database.

To dump the database into an SQL text file::

    pg_dump -h <host> -U <database user> -c <database name> -W > `date +%Y-%m-%d"_"%H-%M-%S`.sql

Example::

    pg_dump -h 127.0.0.1 -U mayan -c mayan -W > `date +%Y-%m-%d"_"%H-%M-%S`.sql

To restore the database from the SQL text file::

    psql -h <host> -U <database user> -d <database name> -W -f <sql dump file>

Example::

    psql -h 127.0.0.1 -U mayan -d mayan -W -f 2018-06-07_18-10-56.sql

Here is an example of how to perform a backup and a restore of a PostgreSQL
Docker container using a compressed dump file. A dump file is not compatible or
can be used interchangeable with an SQL text file.

To backup a PostgreSQL Docker container::

    docker exec <container name> pg_dump -U <database user> -Fc -c <database name> > `date +%Y-%m-%d"_"%H-%M-%S`.dump

Example::

    docker exec mayan-edms-db pg_dump -U mayan -Fc -c mayan > `date +%Y-%m-%d"_"%H-%M-%S`.dump

This will produce a compressed dump file with the current date and time as the filename.

To restore a PostgreSQL Docker container::

    docker exec -i <container name> pg_restore -U <database user> -d <database name> < <dump file>

Since it is not possible to drop a currently open PostgreSQL database, this
command must be used on a new and empty PostsgreSQL container.

Example::

    docker run -d \
    --name mayan-edms-pg-new \
    --restart=always \
    -p 5432:5432 \
    -e POSTGRES_USER=mayan \
    -e POSTGRES_DB=mayan \
    -e POSTGRES_PASSWORD=mayanuserpass \
    -v /docker-volumes/mayan-edms/postgres-new:/var/lib/postgresql/data \
    -d postgres:9.5

    docker exec -i mayan-edms-pg-new pg_restore -U mayan -d mayan < 2018-06-07_17-09-34.dump

More information at:

 - Postgresl: http://www.postgresql.org/docs/current/static/backup.html
 - MySQL: https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html
 - SQLite: Just copy the file ``mayan/media/db.sqlite3``
