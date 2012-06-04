import os
import string
import random

from fabric.api import env
from fabric.colors import green

from literals import (DEFAULT_INSTALL_PATH, DEFAULT_VIRTUALENV_NAME, 
    DEFAULT_REPOSITORY_NAME, DEFAULT_OS, OS_CHOICES, 
    DEFAULT_DATABASE_MANAGER, DB_CHOICES, DEFAULT_DATABASE_NAME,
    DEFAULT_WEBSERVER, WEB_CHOICES, DEFAULT_DATABASE_USERNAME,
    DJANGO_DB_DRIVERS, DEFAULT_DATABASE_HOST, DEFAULT_PASSWORD_LENGTH)
from server_config import reduce_env


def password_generator():
    # http://snipplr.com/view/63223/python-password-generator/
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for x in range(DEFAULT_PASSWORD_LENGTH))


@reduce_env
def setup_environment():
    env['os'] = getattr(env, 'os', DEFAULT_OS)
    env['os_name'] = OS_CHOICES[env.os]
    
    env['install_path'] = getattr(env, 'install_path', DEFAULT_INSTALL_PATH[env.os])
    env['virtualenv_name'] = getattr(env, 'virtualenv_name', DEFAULT_VIRTUALENV_NAME[env.os])
    env['repository_name'] = getattr(env, 'repository_name', DEFAULT_REPOSITORY_NAME[env.os])
    env['virtualenv_path'] = os.path.join(env.install_path, env.virtualenv_name)
    env['repository_path'] = os.path.join(env.virtualenv_path, env.repository_name)
    
    env['database_manager'] = getattr(env, 'database_manager', DEFAULT_DATABASE_MANAGER)
    env['database_manager_name'] = DB_CHOICES[env.database_manager]
    env['database_username'] = getattr(env, 'database_username', DEFAULT_DATABASE_USERNAME)
    env['database_password'] = getattr(env, 'database_password', password_generator())
    env['database_host'] = getattr(env, 'database_host', DEFAULT_DATABASE_HOST)
    env['drop_database'] = getattr(env, 'drop_database', False)
    
    if not getattr(env, 'database_manager_admin_password', None):
        print('Must set the database_manager_admin_password entry in the fabric settings file (~/.fabricrc by default)')
        exit(1)
        
    env['database_name'] = getattr(env, 'database_name', DEFAULT_DATABASE_NAME)

    env['webserver'] = getattr(env, 'webserver', DEFAULT_WEBSERVER)
    env['webserver_name'] = WEB_CHOICES[env.webserver]

    env['django_database_driver'] = DJANGO_DB_DRIVERS[env.database_manager]


def print_supported_configs():
    print('Supported operating systems (os=): %s, default=\'%s\'' % (dict(OS_CHOICES).keys(), green(DEFAULT_OS)))
    print('Supported database managers (database_manager=): %s, default=\'%s\'' % (dict(DB_CHOICES).keys(), green(DEFAULT_DATABASE_MANAGER)))
    print('Supported webservers (webserver=): %s, default=\'%s\'' % (dict(WEB_CHOICES).keys(), green(DEFAULT_WEBSERVER)))
    print('\n')
    
    

    
