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
