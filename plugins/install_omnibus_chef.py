from fabric.api import sudo, hide
#from littlechef import runner as lc

def execute(node):
    """
    Removes the opscode repo
    Installs omnibus Chef
    """

    #env.linewise = True
    with hide('everything'):

        chef_binaries = ['chef-client', 'chef-solo', 'knife', 'ohai', 'shef']
        for binary in chef_binaries:
            sudo('rm -f /usr/local/bin/{0}'.format(binary))
        sudo('apt-get update')
        sudo('apt-get -y install curl')
        sudo('rm -f /etc/apt/sources.list.d/opscode.list')

    sudo('apt-get -y install chef')
    sudo('apt-get -y autoremove')
