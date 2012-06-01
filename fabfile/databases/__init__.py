from fabric.api import env, task
from fabric.colors import green


from ..literals import DB_MYSQL
import mysql


@task
def create_database():
    """
    Create the Mayan EDMS database
    """
    print(green('Creating Mayan EDMS database', bold=True))
    
    if env.database_manager == DB_MYSQL:
        mysql.create_database()


@task
def drop_database():
    """
    Drop Mayan EDMS's database
    """
    print(green('Droping Mayan EDMS database', bold=True))

    if env.database_manager == DB_MYSQL:
        mysql.drop_database()


@task
def drop_username():
    """
    Drop Mayan EDMS's username
    """
    print(green('Droping Mayan EDMS username', bold=True))

    if env.database_manager == DB_MYSQL:
        mysql.drop_username()
