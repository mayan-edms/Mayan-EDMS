import sys

from fabric.api import task, env
from fabric.colors import white

import databases as database
import platforms as platform
import webservers as webserver
import django
import mayan_edms
from conf import print_supported_configs
from server_config import servers

print(white('\n\n          ########          ', bold=True))
print(white('          ########          ', bold=True))
print(white('          ###  ###          ', bold=True))
print(white('        #####  #####        ', bold=True))
print(white('       ##############       ', bold=True))
print(white('      #######  #######      ', bold=True))
print(white('     ##################     ', bold=True))
print(white('    #########  #########    ', bold=True))
print(white('   ######################   ', bold=True))
print(white('  ###########  ###########  ', bold=True))
print(white(' ########################## ', bold=True))
print(white('#############  #############', bold=True))

print(white('\nMayan EDMS Fabric installation file\n\n', bold=True))

print_supported_configs()


@task
def install():
    """
    Perform a complete install of Mayan EDMS on a host
    """
    platform.install_dependencies()
    platform.install_mayan()
    platform.install_database_manager()
    database.create_database()
    database.create_user()
    django.database_config()
    django.syncdb()
    django.collectstatic()
    platform.fix_permissions()
    platform.install_webserver()
    webserver.install_site()
    webserver.restart()
    platform.post_install()

'''
# Disabled until properly implemented
@task
def upgrade():
    """
    Perform a Mayan EDMS installation upgrade
    """
    mayan_edms.upgrade()
'''

@task
def uninstall():
    """
    Perform a complete removal of Mayan EDMS from a host
    """
    platform.delete_mayan()
    webserver.remove_site()
    webserver.restart()

    if env.drop_database:
        database.drop_database()
        database.drop_user()
