from fabric.api import env, task

from ..literals import DB_MYSQL
import mysql


@task
def create_database():
    """
    Create the Mayan EDMS database
    """
    
    if env.database_manager == DB_MYSQL:
        mysql.create_database()


@task
def drop_database():
    """
    Drop Mayan EDMS's database
    """

    if env.database_manager == DB_MYSQL:
        mysql.drop_database()

