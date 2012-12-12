from fabric.api import env, task, cd, sudo, settings
from fabric.colors import green, red

from ..conf import setup_environment


@task
def upgrade():
    """
    Upgrade a Mayan EDMS installation from version v0.12.2 to v0.12.3
    """
    setup_environment()
    print(green('Upgrading Mayan EDMS database from version 0.12.2 to 0.12.3', bold=True))
    #TODO: upgrade steps
