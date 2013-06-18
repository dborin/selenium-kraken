include_recipe 'selenium::default'

case node['kernel']['machine']
when 'i686'
  arch = 'linux32'
when 'x86_64'
  arch = 'linux64'
end

bash "get_chrome_browser" do
  action :run
  user "root"
  code <<-EOH
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
apt-get update
  EOH
end

package 'chromium-browser' do
  action :purge
end

package 'google-chrome-stable' do
  action :upgrade
  notifies :run, "bash[create_chrome_symlink]", :immediately
end

bash "create_chrome_symlink" do
  action :nothing
  user "root"
  cwd "/usr/bin"
  code <<-EOH
if [ -f "/usr/bin/chrome" ]
then
  rm -f /usr/bin/chrome
fi
ln -s /usr/bin/google-chrome /usr/bin/chrome
  EOH
end

package 'unzip'

ARCHIVE="chromedriver_#{arch}_#{node['selenium']['chromedriver_version']}.zip"
SELUSER="#{node['selenium']['user']}"

remote_file "/usr/src/#{ARCHIVE}" do
  source "http://chromedriver.googlecode.com/files/#{ARCHIVE}"
  action :create_if_missing
  notifies :run, "bash[unpack_chromedriver]", :immediately
end

bash "unpack_chromedriver" do
  action :nothing
  user "root"
  cwd "/usr/local/bin"
  code <<-EOH
unzip -o /usr/src/#{ARCHIVE}
chmod -R 0755 /usr/local/bin/chromedriver
chown -R #{SELUSER}:#{SELUSER} /usr/local/bin/chromedriver
  EOH
end
