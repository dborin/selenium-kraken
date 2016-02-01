from fabric.api import sudo
#from littlechef import runner as lc

def execute(node):
    sudo('apt-get -y install ruby-dev')
    sudo('apt-get -y autoremove')
