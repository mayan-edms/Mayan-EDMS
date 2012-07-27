OS_UBUNTU = 'ubuntu'
OS_REDHAT = 'redhat'
OS_CENTOS = 'centos'
OS_FEDORA = 'fedora'
OS_WINDOWS = 'windows'
OS_FREEBSD = 'freebds'
OS_DEBIAN = 'debian'

OS_CHOICES = {
    OS_UBUNTU: 'Ubuntu',
    OS_FEDORA: 'Fedora',
    OS_DEBIAN: 'Debian',
    #OS_REDHAT: 'RedHat',
    #OS_CENTOS: 'CentOS',
    #OS_WINDOWS: 'MS Windows',
    #OS_FREEBSD: 'FreeBSD',
}

DEFAULT_INSTALL_PATH = {
    OS_UBUNTU: '/usr/share',
    OS_FEDORA: '/usr/share',
    OS_DEBIAN: '/usr/share',
}

DEFAULT_VIRTUALENV_NAME = {
    OS_UBUNTU: 'mayan',
    OS_FEDORA: 'mayan',
    OS_DEBIAN: 'mayan',
}

DEFAULT_REPOSITORY_NAME = {
    OS_UBUNTU: 'mayan',
    OS_FEDORA: 'mayan',
    OS_DEBIAN: 'mayan',
}

DB_MYSQL = 'mysql'
DB_PGSQL = 'pgsql'
DB_SQLITE = 'sqlite'
DB_ORACLE = 'oracle'

DB_CHOICES = {
    DB_MYSQL: 'MySQL',
    #DB_PGSQL: 'PostgreSQL',
    #DB_SQLITE: 'SQLite',
    #DB_ORACLE: 'ORACLE'
}

DJANGO_DB_DRIVERS = {
    DB_MYSQL: 'mysql',
    DB_PGSQL: 'postgresql_psycopg2',
    DB_SQLITE: 'sqlite3',
    DB_ORACLE: 'oracle',
}

WEB_APACHE = 'apache'
WEB_NGINX = 'nginx'

WEB_CHOICES = {
    WEB_APACHE: 'Apache',
    #WEB_NGINX: 'Nginx',
}

DEFAULT_OS = OS_UBUNTU
DEFAULT_DATABASE_MANAGER = DB_MYSQL
DEFAULT_DATABASE_NAME = 'mayan'
DEFAULT_WEBSERVER = WEB_APACHE
DEFAULT_DATABASE_USERNAME = 'mayan'
DEFAULT_DATABASE_HOST = '127.0.0.1'
DEFAULT_PASSWORD_LENGTH = 10

FABFILE_MARKER = 'fabfile_install'
