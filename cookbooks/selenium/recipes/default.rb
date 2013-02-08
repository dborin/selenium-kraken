
USER=node['selenium']['user']

group USER

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
end

link File.join(node['selenium']['server']['installpath'], 'selenium-server-standalone.jar') do
  to File.join(node['selenium']['server']['installpath'], "selenium-server-standalone-#{node['selenium']['server']['version']}.jar")
end
