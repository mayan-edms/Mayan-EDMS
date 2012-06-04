from fabric.api import run, env, task, settings
from fabric.colors import green


def create_database():
    """
    Create the MySQL Mayan EDMS database
    """
    run('echo "CREATE DATABASE %(database_name)s;" |  mysql -u root --password=%(database_manager_admin_password)s' % env)
    run('echo "CREATE USER \'%(database_username)s\'@\'%(database_host)s\' IDENTIFIED BY \'%(database_password)s\';" |  mysql -u root --password=%(database_manager_admin_password)s' % env)
    run('echo "GRANT ALL PRIVILEGES ON %(database_name)s.* TO \'%(database_username)s\'@\'%(database_host)s\' WITH GRANT OPTION;" |  mysql -u root --password=%(database_manager_admin_password)s' % env)

    print(green('Password used for Mayan EDMS database account: %s' % env.database_password, bold=True))


def drop_database():
    """
    Drop MySQL's Mayan EDMS's database
    """
    with settings(warn_only=True):
        run('echo "DROP DATABASE %(database_name)s;" |  mysql -u root --password=%(database_manager_admin_password)s' % env)


def drop_username():
    """
    Drop MySQL's Mayan EDMS's username
    """
    with settings(warn_only=True):
        run('echo "DROP USER \'%(database_username)s\'@\'%(database_host)s\';" |  mysql -u root --password=%(database_manager_admin_password)s' % env)

