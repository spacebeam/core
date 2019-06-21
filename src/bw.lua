#!/usr/bin/env luajit

--
-- Bot War in a Singularity Container
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
   epilog = "It can download and launch bots that use BWAPI to communicate with the game."
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

-- Execute some stuff inside the computer OS
local run = "singularity run --writable " .. args['directory']
local start = "singularity instance.start --writable " .. args['directory']
local stop = "singularity instance.stop " .. args['directory']

-- Do your stuff
if args['command'] == 'status' then
    if args['unit'] then
        print('Getting the status of unit ' .. args['unit'] )
        -- status
        print('Done.. ' .. messages[math.random(#messages)])
    else
        os.execute("singularity instance.list")
        os.execute(spawn .. release .. " ping")
    end
-- PLAY, PLAY, PLAY
elseif args['command'] == 'play' then
    if args['unit'] then
        if args['execute'] then
            os.execute(run .. args['unit'] .. ' ' .. args['execute'])
        else
            os.execute(run .. args['unit'])
        end
    else
        print('Did you forget about the ' .. messages[4])
    end
else
    -- do something else
    print(messages[1])
end
