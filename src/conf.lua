-- add work on yml
local yml = require("./lib/YAMLParserLite")

local tools = require("tools")

local raw = tools.read_file("../include/bw.yml")

local conf  = yml.parse(raw)

print(conf)

-- add work on bwapi.ini
local ini = require("inifile")

-- BWAPI and TorchCraft use .ini files
bwapi = ini.parse("../include/bwapi-data/bwapi.ini")

-- Your local variables
local directory = conf["starcraft"]

print(directory)

local bots = directory .. '/bots/'
local games = directory .. '/games/'
local maps = directory .. '/maps/'
local errors = directory .. '/Errors/'
local bwapi_data = directory .. '/bwapi-data/'
local bwapi_save = bwapi_data .. 'save'
local bwapi_read = bwapi_data .. "read"
local bwapi_write = bwapi_data .. "write"
local bwapi_ai = bwapi_data .. "AI"
local bwapi_logs = bwapi_data .. "logs"

-- BWAPI version 4.2.0 and higher ONLY
-- FIRST (default), use the first character in the list
-- WAIT, stop at this screen
-- else the character with the given value is used/created
local character_name = "FIRST"
-- BWAPI version 4.2.0 and higher ONLY
-- Text that appears in the drop-down list below the Game Type.
local game_type_extra = ""

print(bots)

print(games)

print(maps)

print(bwapi_ai)

print(bwapi)
