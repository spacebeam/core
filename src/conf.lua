-- add work on yml
local yml = require("./lib/YAMLParserLite")

local tools = require("tools")

local nice = tools.read_file("../include/bw.yml")

local test = yml.parse(nice)

print(test)

-- add work on bwapi.ini


print("qtuanis")
