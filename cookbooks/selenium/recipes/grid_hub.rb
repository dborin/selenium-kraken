include_recipe 'selenium::default'
include_recipe 'java'
include_recipe 'runit'

template File.join(node['selenium']['server']['installpath'], 'hubConfig.json') do
  source "hubConfig.json.erb"
  mode 0644
  owner node['selenium']['user']
  group node['selenium']['user']
end

runit_service "selenium-hub" do
  default_logger true
end
