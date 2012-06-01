import os

from fabric.api import env

from literals import (DEFAULT_INSTALL_PATH, DEFAULT_VIRTUALENV_NAME, 
    DEFAULT_REPOSITORY_NAME, DEFAULT_OS, OS_CHOICES, 
    DEFAULT_DATABASE_MANAGER, DB_CHOICES, DEFAULT_DATABASE_NAME,
    DEFAULT_WEBSERVER, WEB_CHOICES)


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
    
    if not getattr(env, 'database_manager_admin_password', None):
        print('Must set the database_manager_admin_password entry in the fabric settings file (~/.fabricrc by default)')
        exit(1)
        
    env['database_name'] = getattr(env, 'database_name', DEFAULT_DATABASE_NAME)

    env['webserver'] = getattr(env, 'webserver', DEFAULT_WEBSERVER)
    env['webserver_name'] = WEB_CHOICES[env.webserver]
