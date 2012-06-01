import sys
import os

from fabric.api import run, sudo, cd, env, task
from fabric.main import load_settings

import databases
import webservers
import platforms
from conf import setup_environment

setup_environment()


@task(default=True)
def install():
    platforms.install_dependencies()
    platforms.install_mayan()
    platform.install_database_manager()
    databases.create_database()
    platforms.fix_permissions()
    platforms.install_webserver()
    webservers.install_site()
    webservers.restart()
    

@task
def uninstall():
    platforms.uninstall()
    webservers.remove_site()

    if env.drop_database:
        databases.drop()


