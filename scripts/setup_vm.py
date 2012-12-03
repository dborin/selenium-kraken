import os
import sys
import time

from littlechef import runner as lc
from plumbum import local, FG
from ssh.config import SSHConfig
import ConfigParser

# github.com/racker/vmrunwrapper
import vmrunwrapper

image_url = "http://04dc1fe0f852314a412a-59cce4bc2c52fb076478833b4d47755d.r41.cf1.rackcdn.com/stretch.tar.gz"

script_location = os.path.dirname(__file__)


def parse_littlechef_config(path=None):
    """
    Parse littlechef "config.cfg"
    """
    parser = ConfigParser.SafeConfigParser()
    parser.read(path or os.path.join(script_location, '../config.cfg'))

    try:
        lc.env.user = parser.get('userinfo', 'user')
    except:
        lc.env.user = 'vmuser'

    try:
        lc.env.password = parser.get('userinfo', 'password')
    except:
        lc.env.password = 'vmuser'

    try:
        lc.env.node_work_path = parser.get('kitchen', 'node_work_path')
    except:
        lc.env.node_work_path = "/tmp/chef-solo/"

    lc.env.loglevel = 'debug'
    lc.env.verbose = True


def download_vm(download_to):
    """
    Downloads the VM image
    """
    if os.path.exists(download_to):
        print "VMware image already downloaded."
    else:
        # download the image
        print "Downloading VM image..."
        local['curl']['-o', download_to, image_url] & FG


def get_vm(wrapper):
    """
    Downloads the VM image, copies it to the right location, and takes a
    snapshot.

    If a VM image already exists at the target, shuts that VM down, takes a
    snapshot, and moves it to a backup location before setting up the new VM
    image.
    """
    download_to = os.path.join(script_location, 'stretch.tar.gz')
    download_vm(download_to)

    # make sure the image can be moved into the vmware image directory
    target = os.path.dirname(wrapper.image_location)

    if not os.path.exists(vmrunwrapper.image_locations):
        print "- Making {0} directory.".format(vmrunwrapper.image_locations)
        os.makedirs(vmrunwrapper.image_locations)

    if os.path.exists(target):
        backup = 'stretch.{0}.backup.vmwarevm'.format(time.time())
        print "! stretch.vmwarevm already exists - moving it to {0}".format(
            backup)

        # shut down the old vm
        if wrapper.is_running():
            wrapper.snapshot("Pre_retiring_image")
            wrapper.down()

        # move the vm to a different location
        os.rename(target, os.path.join(vmrunwrapper.image_locations, backup))

    # move the image to the vmware images directory
    print "* Extracting {0} to {1}".format(download_to,
                                         vmrunwrapper.image_locations)
    local['tar']('-C', vmrunwrapper.image_locations, '-xzf', download_to)

    wrapper.snapshot("Post_downoad")


def initialize_vm(wrapper, link_directories=None):
    """
    The VM should have already been downloaded.  This generates SSH keys for
    the user, copies them over, starts the VM, and uses littlechef to bootstrap
    chef solo and required packages.

    Also, it links whatever directories are specified.
    """
    wrapper.generate_ssh_key()
    wrapper.start()
    wrapper.copy_ssh_key(password=lc.env.password)
    wrapper.save_config(os.path.join(script_location, "vmrunwrapper.conf"))

    lc.env.host_string = lc.env.host = wrapper.host
    lc.env.ssh_config_path = wrapper.ssh_config_path
    # set littlechef's ssh config
    lc.env.ssh_config = SSHConfig()
    with open(wrapper.ssh_config_path) as ssh_config:
        lc.env.ssh_config.parse(ssh_config)

    # deploy chef solo
    lc.deploy_chef(ask='no')
    lc.role('base')  # Applies base role to vmware
    # with lib.credentials():
    #     lc.plugin('save_network')

    if link_directories is not None:
        wrapper.share_folders([(directory) for directory in link_directories])

    # take a snapshot
    wrapper.snapshot("Post_Littlechef_Bootstrap")


if __name__ == "__main__":
    parse_littlechef_config()
    wrapper = vmrunwrapper.VmrunWrapper("stretch",
                                        host='vmware',
                                        username=lc.env.user)
    get_vm(wrapper)
    initialize_vm(wrapper, *sys.argv[1:])
