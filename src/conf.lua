-- add work on yml
local yml = require("./lib/YAMLParserLite")

local tools = require("tools")

local nice = tools.read_file("../include/bw.yml")

local test = yml.parse(nice)

print(test)

-- add work on bwapi.ini
local ini = require("inifile")
-- BWAPI and TorchCraft use .ini files

-- Your local variables
local directory = test["starcraft"]

print(directory)

local bots = 'bots/'
local games = 'games/'
local maps = 'maps/'
local errors = 'Errors/'
local bwapi_data = 'bwapi-data/'
local bwapi_save = 'bwapi-data/save'
local bwapi_read = "bwapi-data/read"
local bwapi_write = "bwapi-data/write"
local bwapi_ai = "bwapi-data/AI"
local bwapi_logs = "bwapi-data/logs"

print("qtuanis")
