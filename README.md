# starcraft-sif
This software is a tool for running StarCraft AI competitions inside a [SIF](https://github.com/sylabs/singularity) file based container image, auditable, secure, and easy to move using existing data mobility paradigms.

It can download and launch Win32 C++ and Java bots or any Linux® bot with support for BWAPI `4.1.2, 4.2.0, 4.4.0`.

It uses a server/client architecture with the host acting as a server and any number of other containers acting as clients.

All data send and received pass through ZMQ sockets, no special network configuration is required to run the software.

This repository includes several requirements such as BWAPI.dll files which will automatically be configured and run.

### Serverless
When running the software, the host machine acts as a central repository where all bot files (including file I/O) data, cumulative results, and replays are stored.

The server program has an independent process which monitors for new container connections and detects disconnections, maintaining a current list of instances acting as clients which can have one of the following status:

- **READY**, free and ready to start,
- **STARTING**, the match has not yet begun,
- **RUNNING**, client is running a game,
- **SENDING**, results and data back to the server.

Normally a new game can be started only if:

1. two or more clients are **READY**, and 
2. no clients are **STARTING**.

Once these two conditions are met, the server sends the required bot files, map and BWAPI.dll to the clients, specifying one as the host and another as the away machine. Those client's status are then set to **STARTING**.

### Clients
Each client is handled by independent processes, and if the client is **STARTING**, **RUNNING**, or **SENDING**, it sends periodic status updates back for remote monitoring.

When a game finishes the results are sent back along with file I/O data and replay files, which are stored on the server. 

This process repeats until the competition has finished.

## Getting started
Your system need the latest release of Erlang, LuaJIT (with luarocks) and Singularity installed.

### Installation
Then run this command:

`luarocks install exp`

`exp -u starcraft install`

## Good luck, have fun 

Play against [Ophelia](https://liquipedia.net/starcraft/Ophelia) or any other bot on competitive maps.
```
$ exp -u starcraft run -x "Ophelia"
```

## Settings
All configuration is done in /opt/bw/include/bw.yml. This file must parse as valid [YAML](http://yaml.org) or the competition will not start.

<table>
<tr><th>Name</th><th>Value</th></tr>
<tr>
    <td>starcraft</td>
    <td>
        <b>Type:</b> String<br><br>
        Location of StarCraft: Brood War 1.16.1.
    </td>
</tr>
<tr>
    <td>bots</td>
    <td>
        <b>Type:</b> List of strings<br><br>
        These are the bots that will play in the competition.
        Each bot directory must contain a valid bot.yml file with the following name/value pairs:
        <ul>
        <li><b>name:</b> String name of the bot, matching the bot directory name</li>
        <li><b>race:</b> Terran, Zerg, Protoss, Random</li>
        <li><b>type:</b> Java, DLL, EXE, Linux</li>
        <li><b>bwapi:</b> 4.1.2, 4.2.0, 4.4.0</li>
        </ul>
    </td>
</tr>
<tr>
    <td>maps</td>
    <td>
        <b>Type:</b> List of strings<br><br>
        Each round will be played on these maps at random order. The value should be the name of the map.
    </td>
</tr>
<tr>
    <td>host</td>
    <td>
        <b>Type:</b> String<br><br>
        Host server address.
    </td>
</tr>
<tr>
    <td>port</td>
    <td>
        <b>Type:</b> Number<br><br>
        Port to listen for clients on. 
    </td>
</tr>
<tr>
    <td>speed</td>
    <td>
        <b>Type:</b> String<br><br>
        Allowed values: Slowest, Slower, Slow, Normal, Fast, Faster, Fastest<br><br>
        This changes the speed slider in the game creation lobby it affects the number of latency frames in the game.
    </td>
</tr>
</table>

Example /opt/bw/include/bw.yml:

```yaml
starcraft: /opt/StarCraft
bots:
    - Ophelia
maps:
    - Fighting Spirit
host: 127.0.0.1
port: 58008
speed: Normal
```
## Help wanted
Would you like to help with the project? Pick any of the issues tagged [help wanted](https://github.com/spacebeam/starcraft-sif/labels/help%20wanted) and contribute!

## Contributing
See  [Contributing](CONTRIBUTING.md).
