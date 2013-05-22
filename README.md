# Selenium Server + iNova + littlechef

This repo contains cookbooks for installing a Selenium Server hub or node in a Rackspace iNova environment.  It also requires Java and Python be installed, so those cookbooks are included.  In light of issues with Oracle SDK, OpenSDK is utilized (by default)

## Notes

The following must be configured prior to installation

1. Install `littlechef` on your local machine
2. Since the iNova environment doesn't have any "real" DNS, you will need to
	* Create a local `~/.ssh/chef.config` file that has entries for the Hostnames and IPs of **YOUR** iNova servers that points to whatever private key you're going to use<br><br>	
	
			Host my-hub0
				Hostname 10.14.208.255
				user root
				IdentityFile /Users/ltorvalds/.ssh/secretkey_rsa
			
			Host 10.14.208.255
				user root
				IdentityFile /Users/ltorvalds/.ssh/secretkey_rsa
				
3. Create a `/nodes/*.json` with the following for your hub (and nodes)<br><br>

			{
    			"ipaddress": "10.14.210.137",
    			"name": "10.14.210.137",
    			"run_list": ["role[se-hub]"]
			}
   You will need to change the role in the `run_list` entry from "se-hub" to "se-node" when creating the JSON file for a node.		
4. Create a server (Ubuntu 12.04) for a hub and at least one for a node (multiple nodes can be created), most likely in iNova
5. Append the `secretkey_rsa.pub` to the `/root/.ssh/authorized_keys2` file on all hub and node servers<br><br>

		cat ~/.ssh/secretkey_rsa.pub | { read x; ssh root@my-hub0 "echo $x >> .ssh/authorized_keys2"; }

## Installation

`bootstrap.py` can be run to install either a hub or node.

	./bootstrap.py -H my-hub0

## Tools
[chef](http://wiki.opscode.com/display/chef/Home)<br>
[littlechef](https://github.com/tobami/littlechef)<br>
