# starcraft-sif
This software is a tool for running StarCraft AI competitions inside a [SIF](https://github.com/sylabs/singularity) file based container image, auditable, secure, and easy to move using existing data mobility paradigms.

It can download and launch Win32 C++ and Java bots or any Linux® bot with support for BWAPI `4.1.2, 4.2.0, 4.4.0`.

It uses a server/client architecture with the host acting as a server and any number of other containers acting as clients.

The system is written in a mixture of languages and can be run on Debian 10 or higher, either on a physical machine or a virtual machine.

All data send and received pass through ZMQ sockets, so no special network configuration is required to run the software.

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

Once these two conditions are met, the server sends the required bot files, map, BWAPI.dll and TM.dll to the clients, specifying one as the host and another as the away machine. Those client's status are then set to **STARTING**.

### Clients
Each client is handled by independent processes, and if the client is **STARTING**, **RUNNING**, or **SENDING**, it sends periodic status updates back for remote monitoring.

When a game finishes the results are sent back along with file I/O data and replay files, which are stored on the server. 

This process repeats until the competition has finished.

## Getting started
Your system need the latest release of Erlang, LuaJIT (with luarocks) and Singularity installed.

### Installation
Then run this command:

`luarocks install experience`

`exp -u starcraft install`

## Headless play

Launch headless play of [Ophelia](https://liquipedia.net/starcraft/Ophelia) and [BananaBrain](https://liquipedia.net/starcraft/BananaBrain) on current maps.
```
$ exp -u starcraft run -x "Ophelia BananaBrain"
```

## Settings
All configuration is done in /etc/bw.yml. This file must parse as valid [YAML](http://yaml.org) or the competition will not start.

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
        This changes the speed slider in the game creation lobby.
        The actual speed will be overridden by the tournament.local_speed setting, but the slider affects the number of latency frames in the game.
    </td>
</tr>
<tr>
    <td>tournament<br>.module</td>
    <td>
        <b>Type:</b> String<br><br>
        The Tournament Module DLL which is injected into each StarCraft instance with BWAPI.
        It controls game speed, and outputs data about the game being played so that the client can tell if a bot has crashed, timed out, etc.
    </td>
</tr>
<tr>
    <td>tournament<br>.local_speed</td>
    <td>
        <b>Type:</b> Number<br><br>
        BWAPI Local Speed; Calls BWAPI::Broodwar->setLocalSpeed(SpeedValue).
        Set to 0 to run games at the fastest speed possible.
    </td>
</tr>
<tr>
    <td>tournament<br>.frame_skip</td>
    <td>
        <b>Type:</b> Number<br><br>
        BWAPI Frame Skip; Calls BWAPI::Broodwar->setFrameSkip(SkipValue)<br>
        This does nothing unless LocalSpeed is 0.
    </td>
</tr>
<tr>
    <td>tournament<br>.frame_limit</td>
    <td>
        <b>Type:</b> Number<br><br>
        Game Frame Time Limit; Game stops when BWAPI::Broodwar->getFrameCount() > FrameLimit<br>
        If gameFrameLimit is 0, no frame limit is used.
        Normal Starcraft speed is 24 frames per second.
    </td>
</tr>
<tr>
    <td>tournament<br>.timeouts</td>
    <td>
        <b>Type:</b> List of objects<br><br>
        Each  object must contain the following name/value pairs:
        <ul>
            <li><b>time:</b> Number</li>
            <li><b>frame:</b> Number</li>
        </ul>
        A bot loses a game if it takes <b>time</b> or more to advance a single frame <b>frame</b> times.
        Timeouts of more than 60,000 ms will not have an effect since timeouts of more than a minute are counted as crashes.
    </td>
</tr>
</table>

Example /etc/bw.yml:

```yaml
# The Computer League YAML file 
starcraft: /opt/StarCraft
bots:
    - Ophelia
    - BananaBrain
maps:
    - Circuit Breaker
    - Fighting Spirit
    - Overwatch
    - Tres Pass
    - Power Bond
    - Tau Cross
host: 127.0.0.1
port: 1337
speed: Normal
# tm.dll configuration
tournament:
    module: bwapi-data/tm.dll
    local_speed: 42 
    frame_skip: 256
    frame_limit: 85714
    timeouts:
        -
            time: 55
            frame: 320
        - 
            time: 1000
            frame: 10
        -
            time: 10000
            frame: 1
```
## Help wanted
Would you like to help with the project? Pick any of the issues tagged [help wanted](https://github.com/spacebeam/starcraft-sif/labels/help%20wanted) and contribute!

## Contributing
See  [Contributing](CONTRIBUTING.md).
