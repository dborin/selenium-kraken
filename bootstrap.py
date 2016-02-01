#!/usr/bin/env python

from optparse import OptionParser
from littlechef import runner as lc
from ssh.config import SSHConfig as _SSHConfig
import os
import re
import sys

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

    (options, args) = parser.parse_args()

    checkRequiredArguments(options, parser)

    # begin hackery to load config file until littlechef gets fixed (04DEC2012)

    ssh_config = "~/.ssh/chef.config"
    lc.env.use_ssh_config = True
    lc.env.ssh_config = _SSHConfig()
    lc.env.ssh_config_path = os.path.expanduser(ssh_config)

    # end hackery

    lc.env.user = options.username
    lc.env.password = options.password
    lc.env.host_string = options.hostname
    lc.env.host = options.hostname
    lc.env.encrypted_data_bag_secret = None
    lc.env.follow_symlinks = False
    lc.plugin("install_ruby_dev")
    lc.plugin("install_omnibus_chef")
    lc.node(options.hostname)

if __name__=="__main__":
    main()
