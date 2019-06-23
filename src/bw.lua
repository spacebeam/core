#!/usr/bin/env luajit
--
-- StarCraft:Brood War bots running inside a Singularity Linux® Container
--
local argparse = require("argparse")
local socket = require("socket")
local uuid = require("uuid")
-- init random seed
uuid.randomseed(socket.gettime()*10000)
-- Session UUID
local session_uuid = uuid()
-- CLI argument parser
local parser = argparse() {
   name = "bw",
   description = "bw command line toolkit.",
   epilog = "It can download and launch Win32 C++ and Java bots " .. 
   "or any Linux® bot with support for BWAPI 4.1.2, 4.2.0, 4.4.0."
}
-- Spawning bots at directory
local sc = "/opt/StarCraft/"
parser:option("-d --directory", "StarCraft bots directory", sc .. "bots/")
-- Fighting bots
parser:option("-b --bots", "Prepare to fight", "Ophelia Blueberry")
-- Map is not territory
parser:option("-m --map", "for territory", "maps/download/Fighting\\ Spirit.scx")
-- CLI pkg command
parser:command_target("command")
-- How are you? 
parser:command("status")
-- Live for the swarm! 
parser:command("play")
-- Your local variables
local games = sc .. "games/" 
local bwta = sc .. "bwapi-data/BWTA"
local bwta2 = sc .. "bwapi-data/BWTA2"
local maps = sc .. "maps/"
local errors = sc .. "Errors/"
local bwapi_data = sc .. "bwapi-data/"
local bot_data_save = sc .. "bwapi-data/save"
local bot_data_read = sc .. "bwapi-data/read"
local bot_data_write = sc .. "bwapi-data/write"
local bot_data_ai = sc .. "bwapi-data/AI"
local bot_data_logs = sc .. "bwapi-data/logs"
-- Your system messages
local messages = {
  'Can I take your order?',
  'Go ahead HQ.',
  'In the pipe, five by five.',
  'In transit HQ.',
  'I copy that.',
}
-- Parse your arguments
local args = parser:parse()
-- STATUS, STATUS, STATUS 
if args['command'] == 'status' then
    print('status')
-- PLAY, PLAY, PLAY
elseif args['command'] == 'play' then
    print('play')
    print(args['bots'])
    print(args['map'])
    print(args['directory'])
    print(sc)
    print(maps)
else
    -- do something else
    print(messages[1])
end
