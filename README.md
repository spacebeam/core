# starcraft-sif
This software is a tool for running StarCraft AI competitions from Linux running bots inside a [SIF](https://github.com/sylabs/singularity) file based container image, auditable, secure, and easy to move using existing data mobility paradigms.

It can download and launch Win32 C++ and Java bots or any Linux® bot with support for BWAPI `4.1.2, 4.2.0, 4.4.0`.

It uses a server/client architecture with the host acting as a server and any number of other containers acting as clients.

The system is written in a mixture of Lua, Erlang and Python and can be run on Debian 10 or higher, either on a physical machine or a virtual machine.

All data send and received pass through ZMQ sockets, so no special network configuration is required to run the software.

This repository includes several requirements such as BWAPI.dll files which will automatically be configured and run.


### Serverless
When running the software, the host machine acts as a central repository where all bot files (including file I/O) data, cumulative results, and replay files are stored.

The server program has an independent process which monitors for new container connections and detects disconnections, maintaining a current list of instances acting as clients which can have one of the following status:

- READY, free and ready to start,
- STARTING, the match has not yet begun,
- RUNNING, client is running a game,
- SENDING, results and data back to the server.

Normally a new game can be started only if:

1. two or more clients are READY, and 
2. no clients are STARTING.

Once these two conditions are met, the server sends the required bot files, map, BWAPI.dll and TM.dll to the clients, specifying one as the host and another as the away machine. Those client's status are then set to STARTING.

### Clients
Each client is handled by separete processes in the server, and if the client is STARTING, RUNNING, or SENDING, it sends periodic status updates back for remote monitoring.

When a game finishes the results are sent back along with file I/O data and replay files, which are stored on the server. 

This process repeats until the competition has finished.

## Getting started
Your system need the latest release of Erlang, LuaJIT (with luarocks) and Singularity installed.

### Installation
Then run this command:

`luarocks install package`

`pkg -u starcraft install`

## Headless play

Launch headless play of [Ophelia](https://liquipedia.net/starcraft/Ophelia) and [Blueberry](https://liquipedia.net/starcraft/Blueberry) on current maps.
```
$ pkg -u starcraft run -x "Ophelia Blueberry"
```

