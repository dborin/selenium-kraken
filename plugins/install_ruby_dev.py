from fabric.api import sudo
#from littlechef import runner as lc

def execute(node):
    sudo('apt-get -y install ruby1.9.1 ruby-dev dbus-x11')
