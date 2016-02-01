#!/usr/bin/env python

import littlechef
import os
import re
import sys

from littlechef import runner as lc
from optparse import OptionParser
from paramiko.config import SSHConfig as _SSHConfig


def checkRequiredArguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) == None:
            missing_options.extend(option._long_opts)
    if len(missing_options) > 0:
        print ('\nMissing REQUIRED parameters: ' + str(missing_options) + '\n')
        parser.print_help()
        sys.exit(1)

def main():
    parser = OptionParser()
    parser.add_option("-u", "--username", default="root",
        help="username for new server, defaults to %default")
    parser.add_option("-p", "--password", dest="password",
        help="password for new server")
    parser.add_option("-H", "--hostname", dest="hostname",
        help="[REQUIRED] hostname or ip of new server")
    parser.add_option("-e", "--environment", dest="chef_environment",
        help="[REQUIRED] environment for new server (dev, preprod, prod, etc.)")

    (options, args) = parser.parse_args()

    checkRequiredArguments(options, parser)

    dir = os.path.dirname(os.path.abspath(__file__))
    ssh_config = os.path.join(dir, "config/bootstrap-ssh-config")

    lc.env.use_ssh_config = True
    lc.env.ssh_config_path = os.path.expanduser(ssh_config)

    littlechef.runner._readconfig()

    lc.env.user = options.username
    lc.env.password = options.password
    lc.env.host_string = options.hostname
    lc.env.host = options.hostname

    lc.env.chef_environment = options.chef_environment

    lc.env.follow_symlinks = False

    # We need the ohai plugins installed before running Chef
    lc.plugin("install_omnibus_chef")
    lc.plugin("save_cloud")
    lc.plugin("save_network")
    lc.plugin("save_chef_environment")
    lc.role("base")

if __name__=="__main__":
    main()
