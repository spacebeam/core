# starcraft-sif
This software is a tool for running StarCraft AI competitions from Linux running bots inside a [SIF](https://github.com/sylabs/singularity) file based container image, auditable, secure, and easy to move using existing data mobility paradigms.

It can download and launch Win32 C++ and Java bots or any Linux® bot with support for BWAPI `4.1.2, 4.2.0, 4.4.0`.

It uses a server/client architecture with the host acting as a server and any number of other containers acting as clients.

The system is written in a mixture of Lua, Erlang and Python and can be run on Debian 10 or higher, either on a physical machine or a virtual machine.

All data send and received pass through ZMQ sockets, so no special network configuration is required to run the software.

This repository includes several requirements such as BWAPI.dll files which will automatically be configured and run.

## Serverless
When runnin the software, the host machine acts as a server for the competition.

The server is a central repository where all bot files (including file I/O) data, cumulative results, and replay files are stored.

The server program has an independent process which monitors for new container connections and detects disconnections, maintaining a current list of instances acting as clients which can have one of the following statuses:

- READY, free and ready to start
- STARTING, the match has not yet begun
- RUNNING, client is running a game
- SENDING, results and data back to the server

Normally a new game can be started only if:

1. two or more clients are READY, and 
2. no clients are STARTING.

Once these two conditions are met, the server sends the required bot files, map, BWAPI, and TM.dll to the client machines, specifying one client as the host and one as the away machine.

Those client's status are then set to *STARTING*. 

Each client is handled by a separete processes in the server, and if the client is STARTING, RUNNING, or SENDING, it sends periodic status updates back for remote monitoring.

When a game finishes the results are sent back along with file I/O data and replay files, which are stored on the server. This process repeats until the competition has finished.

## Headless play

Launch headless play of [Ophelia](https://liquipedia.net/starcraft/Ophelia) and [Blueberry](https://liquipedia.net/starcraft/Blueberry) on current maps.
```
    $ pkg -u starcraft run -x "Ophelia Blueberry"
```

## Development

### Add your own bot

Place your bot to `--bots` directory. Some of these are inspired by [SSCAIT rules](http://sscaitournament.com/index.php?action=rules).

Use this structure:

- **/AI/** - put your bot binaries here.

- **/read/** - folder where you can put your config files, initial opponent modelling etc.

  It's contents may be overwritten. After running games contents of the write folder can be copied here, see below.

- **/write/** - folder where bot can write.

    Note that `bw` creates subdirectories in write folder, for each game it's own. The contents of the *write/GAME_xxx* folder will be copied to the *read* folder.

- **/bot.yml** - bot configuration. Minimal config is following:

        name: Blueberry 
        race: Terran
        type: Python
        bwapi: 4.2.0

    `name` must match `[a-zA-Z0-9_][a-zA-Z0-9_. -]{0,40}`

    `race` can be one of `Terran`, `Zerg`, `Protoss`, `Random`

    `type` can be one of `Java`, `DLL`, `EXE`, `Python`, `LuaJIT`
    
    `bwapi` can be one of `4.1.2`, `4.2.0`, `4.4.0`
