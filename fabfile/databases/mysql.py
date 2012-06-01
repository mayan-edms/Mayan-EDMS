from fabric.api import run, sudo, cd, env, task


def create_database():
    """
    Create the MySQL Mayan EDMS database
    """
    run('echo "create database %(database_name)s;" |  mysql -u root --password=%(database_manager_admin_password)s' % env)
    #TODO: create DB and mayan user
    #TODO: custom settings_local


def drop_database():
    """
    Drop MySQL's Mayan EDMS's database
    """
    run('echo "drop database %(database_name)s;" |  mysql -u root --password=%(database_manager_admin_password)s' % env)

