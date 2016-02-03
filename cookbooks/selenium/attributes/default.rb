default.selenium.user = 'seleniumuser'
default.selenium.home = '/home/seleniumuser/'

default.selenium.bindings = { 'python' => '2.50.1', 'ruby' => '2.50.1'}

#hub config
default.selenium.server.version = '2.50.1'
default.selenium.server.majmin = '2.50'
default.selenium.server.installpath = default['selenium']['home']+'selenium'
default.selenium.server.standalonefile = default['selenium']['home']+'selenium'

#advanced hub config
default.selenium.server.nodePolling = '5000'
default.selenium.server.cleanUpCycle = '5000'
default.selenium.server.timeout = '300000'
default.selenium.server.maxSession = '15'

#nodes config
default.selenium.server.hubport = '4444'
default.selenium.node.hubhost = 'qa-se-grid.iad.livingsocial.net'
default.selenium.node.port = '5555'
default.selenium.node.maxSession = '15'

default.selenium.xvfb.display = ':98'
default.selenium.xvfb.fbsize = '1280x1024x16'

default.selenium.chromedriver_version = '2.20'
