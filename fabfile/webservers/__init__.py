from fabric.api import run, sudo, cd, env, task

from ..literals import WEB_APACHE
import apache


@task
def install_site():
    """
    Install Mayan EDMS site in the webserver configuration files
    """
    
    print('Adding Mayan EDMS\'s site files to: %s' % os.webserver_name)

    if os.webserver == WEB_APACHE:
        apache.install_site()


@task
def remove_site():
    """
    Install Mayan EDMS's site file from the webserver's configuration
    """    
    print('Removing Mayan EDMS\s site file from %s configuration' % os.webserver_name)

    if os.webserver == WEB_APACHE:
        apache.remove_site()


@task    
def restart():
    """
    Restart the webserver
    """    
    print('Restarting the web server: %s' % os.webserver_name)

    if os.webserver == WEB_APACHE:
        apache.restart()


@task
def reload():
    """
    Reload webserver configuration files
    """    
    print('Reloading the web server configuration files')

    if os.webserver == WEB_APACHE:
        apache.reload()
