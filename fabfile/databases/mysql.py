from fabric.api import run, sudo, cd, env, task


def create_database():
    """
    Create the MySQL Mayan EDMS database
    """
    run('echo "CREATE DATABASE %(database_name)s;" |  mysql -u root --password=%(database_manager_admin_password)s' % env)
    run('echo "CREATE USER \'%(database_username)s\'@\'localhost\' IDENTIFIED BY \'%(database_password)s\';" |  mysql -u root --password=%(database_manager_admin_password)s' % env)
    run('echo "GRANT ALL PRIVILEGES ON %(database_name)s.* TO \'%(database_username)s\'@\'localhost\' WITH GRANT OPTION; |  mysql -u root --password=%(database_manager_admin_password)s' % env)


def drop_database():
    """
    Drop MySQL's Mayan EDMS's database
    """
    run('echo "drop database %(database_name)s;" |  mysql -u root --password=%(database_manager_admin_password)s' % env)

