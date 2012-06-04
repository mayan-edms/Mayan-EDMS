"""Fabric server config management fabfile.
If you need additional configuration, setup ~/.fabricrc file:

    user = your_remote_server_username

To get specific command help type:
    fab -d command_name

"""
# From http://fueledbylemons.com/blog/2011/04/09/server-configs-and-fabric/


import os

from fabric.api import env, task
from fabric.utils import puts
from fabric import colors
import fabric.network
import fabric.state


YAML_AVAILABLE = True
try:
    import yaml
except ImportError:
    YAML_AVAILABLE = False


JSON_AVAILABLE = True
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        JSON_AVAILABLE = False

################################
#         ENVIRONMENTS         #
################################

def _load_config(**kwargs):
    """Find and parse server config file.

    If `config` keyword argument wasn't set look for default
    'server_config.yaml' or 'server_config.json' file.

    """
    config, ext = os.path.splitext(kwargs.get('config',
        'server_config.yaml' if os.path.exists('server_config.yaml') else 'server_config.json'))

    if not os.path.exists(config + ext):
        print colors.red('Error. "%s" file not found.' % (config + ext))
        return {}
    if YAML_AVAILABLE and ext == '.yaml':
        loader = yaml
    elif JSON_AVAILABLE and ext =='.json':
        loader = json
    else:
        print colors.red('Parser package not available')
        return {}
    # Open file and deserialize settings.
    with open(config + ext) as config_file:
        return loader.load(config_file)

@task
def servers(*args, **kwargs):
    """Set destination servers or server groups by comma delimited list of names"""
    # Load config
    servers = _load_config(**kwargs)
    # If no arguments were recieved, print a message with a list of available configs.
    if not args:
        print 'No server name given. Available configs:'
        for key in servers:
            print colors.green('\t%s' % key)

    # Create `group` - a dictionary, containing copies of configs for selected servers. Server hosts
    # are used as dictionary keys, which allows us to connect current command destination host with
    # the correct config. This is important, because somewhere along the way fabric messes up the
    # hosts order, so simple list index incrementation won't suffice.
    env.group = {}
    # For each given server name
    for name in args:
        #  Recursive function call to retrieve all server records. If `name` is a group(e.g. `all`)
        # - get it's members, iterate through them and create `group`
        # record. Else, get fields from `name` server record.
        # If requested server is not in the settings dictionary output error message and list all
        # available servers.
        _build_group(name, servers)


    # Copy server hosts from `env.group` keys - this gives us a complete list of unique hosts to
    # operate on. No host is added twice, so we can safely add overlaping groups. Each added host is
    # guaranteed to have a config record in `env.group`.
    env.hosts = env.group.keys()

def _build_group(name, servers):
    """Recursively walk through servers dictionary and search for all server records."""
    # We're going to reference server a lot, so we'd better store it.
    server = servers.get(name, None)
    # If `name` exists in servers dictionary we
    if server:
        # check whether it's a group by looking for `members`
        if isinstance(server, list):
            if fabric.state.output['debug']:
                    puts("%s is a group, getting members" % name)
            for item in server:
                # and call this function for each of them.
                _build_group(item, servers)
        # When, finally, we dig through to the standalone server records, we retrieve
        # configs and store them in `env.group`
        else:
            if fabric.state.output['debug']:
                    puts("%s is a server, filling up env.group" % name)
            env.group[server['host']] = server
    else:
        print colors.red('Error. "%s" config not found. Run `fab servers` to list all available configs' % name)

def reduce_env(task):
    """
    Copies server config settings from `env.group` dictionary to env variable.

    This way, tasks have easier access to server-specific variables:
        `env.owner` instead of `env.group[env.host]['owner']`

    """
    def task_with_setup(*args, **kwargs):
        # If `s:server` was run before the current command - then we should copy values to
        # `env`. Otherwise, hosts were passed through command line with `fab -H host1,host2
        # command` and we skip.
        if env.get("group", None):
            for key,val in env.group[env.host].items():
                setattr(env, key, val)
                if fabric.state.output['debug']:
                    puts("[env] %s : %s" % (key, val))

        task(*args, **kwargs)
        # Don't keep host connections open, disconnect from each host after each task.
        # Function will be available in fabric 1.0 release.
        # fabric.network.disconnect_all()
    return task_with_setup
