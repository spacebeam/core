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
parser:option("-d --directory", "StarCraft bots directory", "/opt/StarCraft/bots/")
-- Fighting bots
parser:option("-b --bots", "Prepare to fight", "Ophelia Blueberry")
-- Map is not territory
parser:option("-m --map", "for territory", "maps/download/Fighting\\ Spirit.scx")

--
-- CLI pkg command


parser:command_target("command")

-- ?
parser:command("status")

-- execute the game
parser:command("play")

-- Your system variables

-- system messages
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
else
    -- do something else
    print(messages[1])
end
