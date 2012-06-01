import os

from fabric.api import run, sudo, cd, env, task

from fabfiles.databases import mysql
from fabfiles.webservers import apache
from fabfiles.platforms import ubuntu
from fabfiles.conf import setup_paths


@task(default=True)
def install(**kwargs):
    setup_paths(**kwargs)
    
    ubuntu.install_dependencies()
    ubuntu.install_mayan()
    mysql.install_database_manager()
    mysql.create_database()
    ubuntu.fix_permissions()
    apache.install()
    apache.install_site()
    apache.restart()


@task
def uninstall(**kwargs):
    setup_paths(**kwargs)

    ubuntu.uninstall()
    apache.remove_site()


