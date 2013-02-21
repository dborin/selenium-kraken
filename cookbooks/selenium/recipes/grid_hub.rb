include_recipe 'java'
include_recipe 'runit'

USER=node['selenium']['user']

group USER

service "selenium-hub"

user USER do
  comment "selenium user"
  gid USER
  #system true
  shell "/bin/bash"
  home node['selenium']['home']
end

directory node['selenium']['server']['installpath'] do
  owner USER
  recursive true
end

remote_file File.join(node['selenium']['server']['installpath'], "selenium-server-standalone-#{node['selenium']['server']['version']}.jar") do
  source "http://selenium.googlecode.com/files/selenium-server-standalone-#{node['selenium']['server']['version']}.jar"
  action :create_if_missing
  mode 0644
  owner USER
  group USER
  notifies :restart, resources(:service => ["selenium-hub"])
end

link File.join(node['selenium']['server']['installpath'], 'selenium-server-standalone.jar') do
  to File.join(node['selenium']['server']['installpath'], "selenium-server-standalone-#{node['selenium']['server']['version']}.jar")
end

template File.join(node['selenium']['server']['installpath'], 'hubConfig.json') do
  source "hubConfig.json.erb"
  mode 0644
  owner node['selenium']['user']
  group node['selenium']['user']
end

runit_service "selenium-hub" do
  default_logger true
end
