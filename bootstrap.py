from optparse import OptionParser
from littlechef import runner as lc

parser = OptionParser()
parser.add_option("-p", "--password", dest="password",
    help="root password for new server")
parser.add_option("-H", "--hostname", dest="hostname",
    help="hostname or ip of new server")

(options, args) = parser.parse_args()

lc.env.user = 'root'
lc.env.password = options.password
lc.env.host_string = options.hostname
lc.env.host = options.hostname
lc.env.node_work_path = "/tmp/chef-solo/"
lc.deploy_chef()

# We need the ohai plugins installed before running Chef
lc.recipe("ohai")
#lc.plugin("save_network")
#lc.plugin("save_cloud")
#lc.role("prod")
