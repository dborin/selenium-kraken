#!/usr/bin/env python

from optparse import OptionParser
from littlechef import runner as lc
from ssh.config import SSHConfig as _SSHConfig
import os

def main():
    parser = OptionParser()
    parser.add_option("-p", "--password", dest="password",
        help="root password for new server")
    parser.add_option("-H", "--hostname", dest="hostname",
        help="server hostname")

    (options, args) = parser.parse_args()

    # begin hackery to load config file until littlechef gets fixed (04DEC2012)

    ssh_config = "~/.ssh/chef.config"
    lc.env.use_ssh_config = True
    lc.env.ssh_config = _SSHConfig()
    lc.env.ssh_config_path = os.path.expanduser(ssh_config)

    # end hackery

    lc.env.user = 'root'
    lc.env.password = options.password
    lc.env.host_string = options.hostname
    lc.env.host = options.hostname
    lc.deploy_chef()
    lc.node(options.hostname)

if __name__=="__main__":
    main()
