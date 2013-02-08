include_recipe 'selenium::default'
include_recipe 'runit'
package "xvfb"
package "xfonts-base"
package "xfonts-75dpi"
package "xfonts-100dpi"

runit_service "xvfb-service" do
  default_logger true
end
