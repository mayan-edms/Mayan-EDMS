from fabric.api import task, env
from fabric.colors import white

import databases as database
import webservers as webserver
import platforms as platform
import django
from conf import setup_environment

setup_environment()


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


@task(default=True)
def install():
    platform.install_dependencies()
    platform.install_mayan()
    platform.install_database_manager()
    database.create_database()
    django.database_config()
    django.syncdb()
    django.collectstatic()
    platform.fix_permissions()
    platform.install_webserver()
    webserver.install_site()
    webserver.restart()
    

@task
def uninstall():
    platform.delete_mayan()
    webserver.remove_site()
    webserver.restart()

    if env.drop_database:
        database.drop_database()


