include_recipe 'selenium::default'
include_recipe 'java'
include_recipe 'selenium::xvfb'
include_recipe 'runit'


template File.join(node['selenium']['server']['installpath'], 'nodeConfig.json') do
  source "nodeConfig.json.erb"
  mode 0644
  owner node['selenium']['user']
  group node['selenium']['user']
end

runit_service "selenium-node" do
  default_logger true
end
