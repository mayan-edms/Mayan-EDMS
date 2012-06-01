OS_UBUNTU = 'ubuntu'
OS_REDHAT = 'redhat'
OS_CENTOS = 'centos'
OS_FEDORA = 'fedora'
OS_WINDOWS = 'windows'
OS_FREEBSD = 'freebds',

OS_CHOICES = {
    OS_UBUNTU: 'Ubuntu',
    OS_REDHAT: 'RedHat',
    OS_CENTOS: 'CentOS',
    OS_FEDORA: 'Fedora',
    OS_WINDOWS: 'MS Windows',
    OS_FREEBSD: 'FreeBSD',
}

DEFAULT_INSTALL_PATH = {
    OS_UBUNTU: '/usr/share'
}

DEFAULT_VIRTUALENV_NAME = {
    OS_UBUNTU: 'mayan'
}

DEFAULT_REPOSITORY_NAME = {
    OS_UBUNTU: 'mayan'
}

DB_MYSQL = 'mysql'
DB_PGSQL = 'pgsql'
DB_SQLITE = 'sqlite'

DB_CHOICES = {
    DB_MYSQL: 'MySQL',
    DB_PGSQL: 'PostgreSQL',
    DB_SQLITE: 'SQLite'
}

WEB_APACHE = 'apache'
WEB_NGINX = 'nginx'

WEB_CHOICES = {
    WEB_APACHE: 'Apache',
    WEB_NGINX: 'Nginx',
}

DEFAULT_OS = OS_UBUNTU
DEFAULT_DATABASE_MANAGER = DB_MYSQL
DEFAULT_DATABASE_NAME = 'mayan'
DEFAULT_WEBSERVER = WEB_APACHE
