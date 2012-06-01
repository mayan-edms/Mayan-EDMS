from fabric.api import task

import databases as database
import webservers as webserver
import platforms as platform
import django
from conf import setup_environment

setup_environment()


@task(default=True)
def install():
    platform.install_dependencies()
    platform.install_mayan()
    platform.install_database_manager()
    database.create_database()
    django.database_config()
    django.syncdb()
    platform.fix_permissions()
    platform.install_webserver()
    webserver.install_site()
    webserver.restart()
    

@task
def uninstall():
    platform.uninstall()
    webserver.remove_site()

    if env.drop_database:
        database.drop()


