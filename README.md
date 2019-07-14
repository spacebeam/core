# starcraft-sif
This software is a tool for running StarCraft AI competitions inside a [SIF](https://github.com/sylabs/singularity) file based container image, auditable, secure, and easy to move using existing data mobility paradigms.

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

## Settings
All configuration is done in /etc/bw.yml. This file must parse as valid YAML or the competition will not start.

<table>
<tr><th>Name</th><th>Value</th></tr>
<tr>
    <td>bots</td>
    <td>
        <b>Type:</b> Array of json objects<br><br>
        These are the bots that will play in the tournament.
        Each bot object must contain the following name/value pairs:
        <ul>
        <li><b>BotName:</b> String - the name of the bot, matching the bot folder name</li>
        <li><b>Race:</b> "Random" | "Terran" | "Zerg" | "Protoss"</li>
        <li><b>BotType:</b> "dll" | "proxy"</li>
        <li><b>BWAPIVersion:</b> "BWAPI_374" | "BWAPI_401B" | "BWAPI_412" | "BWAPI_420" | "BWAPI_440"</li>
        <li><b>ClientRequirements</b> (OPTIONAL): array of strings with required properties</li>
            <ul>
                <li>Example: ["GPU", "Extra RAM", "!64-bit Java"]</li>
                <li>If the first character of a property is "!", then that bot can only use a client that doesn't have that property. In the example above, the bot could play only on a client with both the "GPU" and "Extra RAM" properties and not the "64-bit Java" property.</li>
                <li>Bot requirements must match a client in the tournament (see Client Settings) or the tournament will not be able to finish</li>
            </ul>
        </ul>
         Example: {"BotName": "UAlbertaBot", "Race": "Random", "BotType": "proxy", "BWAPIVersion": "BWAPI_420"}
    </td>
</tr>
<tr>
    <td>maps</td>
    <td>
        <b>Type:</b> Array of strings<br><br>
        Each round of the tournament will be played on these maps in the order they are listed in. The value should be the path to the map relative to the Starcraft directory; no spaces
         Example: "maps/aiide/(2)Benzene.scx"
    </td>
</tr>
<tr>
    <td>gamesListFile</td>
    <td>
        <b>Type:</b> String<br><br>
        Location of file with list of games to be played, relative to server.jar; No spaces.
        The user will be prompted to generate a new games list if the file does not already exist (i.e. if this is a new tournament).
    </td>
</tr>
<tr>
    <td>resultsFile</td>
    <td>
        <b>Type:</b> String<br><br>
        Location of tournament results file, relative to server.jar. No spaces. Raw results data returned from clients is stored in this file (one line for each client). Nice results are output by the server in the html/ directory.
    </td>
</tr>
<tr>
    <td>detailedResults</td>
    <td>
        <b>Type:</b> Boolean<br><br>
        Setting to true auto-generates detailed results whenever a game result is received.
        Generating detailed results gets slow for very large tournaments, so default is false.
        You can manually generate the results from the Actions menu in the server, which is recommended.
    </td>
</tr>
<tr>
    <td>serverPort</td>
    <td>
        <b>Type:</b> Number<br><br>
        Port to listen for clients on. This should match the port number in the client's <b>ServerAddress</b> setting.
    </td>
</tr>
<tr>
    <td>clearResults</td>
    <td>
        <b>Type:</b> String<br><br>
        Clear existing results on server start? Allowed values: "yes" | "no" | "ask"<br>
        If "yes" then a new tournament is always started when the server is started. If "no" then an existing tournament will be resumed if possible.
    </td>
</tr>
<tr>
    <td>startGamesSimultaneously</td>
    <td>
        <b>Type:</b> Boolean<br><br>
        If set to <b>true</b> new games will be started while other games are still in the starting process (i.e. other Starcraft instances are in the lobby).
        If set to <b>false</b> only one game can be <b>STARTING</b> at a time.<br><br>
        <b>WARNING:</b> This is only usable if all bots are using BWAPI version 4.2.0 or higher.
        If using older versions of BWAPI, bots will join any game in the lobby, leading to games with more than 2 players, and generally games that do not match.
    </td>
</tr>
<tr>
    <td>tournamentType</td>
    <td>
        <b>Type:</b> String<br><br>
        Allowed values: "AllVsAll" | "1VsAll"<br>
        <ul>
            <li>AllVsAll - Standard round robin tournament</li>
            <li>1VsAll - First bot in <b>bots</b> list will play all the others.
             Useful for testing changes to your bot.</li>
        </ul>
    </td>
</tr>
<tr>
    <td>lobbyGameSpeed</td>
    <td>
        <b>Type:</b> String<br><br>
        Allowed values: "Slowest" | "Slower" | "Slow" | "Normal" | "Fast" | "Faster" | "Fastest"<br>
        This setting changes registry entries on the client machines so that the game speed slider in the game creation lobby is set appropriately.
        The actual game speed will be overridden by the tournamentModuleSettings.localSpeed setting, but the slider affects the number of latency frames in the game (the number of frames between a command and its execution).
    </td>
</tr>
<tr>
    <td>enableBotFileIO</td>
    <td>
        <b>Type:</b> Boolean<br><br>
        If set to <b>true</b> the server will wait for each round to complete before sarting the next round.
        Every time a round finishes the contents of 'BotName/write' will be copied to 'BotName/read'.
        Bots that implement learning from previous rounds will have access to the contents of the read directory in 'bwapi-data/read' on the client machine.
        If set to <b>false</b> the server will ignore round numbers when scheduling games, and never copy from 'write' to 'read'.
    </td>
</tr>
<tr>
    <td>ladderMode</td>
    <td>
        <b>Type:</b> Boolean<br><br>
        If set to <b>true</b> enables some alternate functionality designed to work with a persistant online ladder server in development by the authors of this project. Should not be used otherwise.
    </td>
</tr>
<tr>
    <td>excludeFromResults</td>
    <td>
        <b>Type:</b> Array of strings<br><br>
        Bots listed in this array will be excluded from the results summary and detailed results output, but games that include them will still be played.
        This feature is useful if you need to disqualify a bot from a tournament, or want to see the overall effects of a bot on the results.
        The values in this array should match bot names given in the array of competing bots.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings</td>
    <td>
        <b>Type:</b> Object<br><br>
        Tournament Module settings control the tournament module DLL which is injected into each Starcraft instance with BWAPI.
        It controls game speed, draws information to the screen, and outputs data about the game being played so that the client can tell if a bot has crashed, timed out, etc.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings<br>.localSpeed</td>
    <td>
        <b>Type:</b> Number<br><br>
        BWAPI Local Speed; Calls BWAPI::Broodwar->setLocalSpeed(SpeedValue).
        Set to 0 to run games at the fastest speed possible.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings<br>.frameSkip</td>
    <td>
        <b>Type:</b> Number<br><br>
        BWAPI Frame Skip; Calls BWAPI::Broodwar->setFrameSkip(SkipValue)<br>
        This does nothing unless LocalSpeed is 0.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings<br>.gameFrameLimit</td>
    <td>
        <b>Type:</b> Number<br><br>
        Game Frame Time Limit; Game stops when BWAPI::Broodwar->getFrameCount() > FrameLimit<br>
        If gameFrameLimit is 0, no frame limit is used.
        Normal Starcraft speed is 24 frames per second.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings<br>.timeoutLimits</td>
    <td>
        <b>Type:</b> Array of json objects<br><br>
        Each timeoutLimit object must contain the following name/value pairs:
        <ul>
            <li><b>timeInMS:</b> Number</li>
            <li><b>frameCount:</b> Number</li>
        </ul>
        A bot loses a game if it takes <b>timeinMS</b> or more time to advance a single frame <b>frameCount</b> times.
        Timeout limits of more than 60,000 ms will not have an effect since timeouts of more than a minute are counted as crashes.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings<br>.drawBotNames</td>
    <td>
        <b>Type:</b> Boolean<br><br>
        Set to <b>true</b> to draw bot names on the game screen.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings<br>.drawTournamentInfo</td>
    <td>
        <b>Type:</b> Boolean<br><br>
        Set to <b>true</b> to draw tournament information on the game screen.
    </td>
</tr>
<tr>
    <td>tournamentModuleSettings<br>.drawUnitInfo</td>
    <td>
        <b>Type:</b> Boolean<br><br>
        Set to <b>true</b> to draw unit information on the game screen.
    </td>
</tr>
</table>

Example server_settings.json:

```json
{
    "bots": [
        {"BotName": "UAlbertaBot", "Race": "Random", "BotType": "proxy", "BWAPIVersion": "BWAPI_420"},
        {"BotName": "ExampleBot", "Race": "Protoss", "BotType": "dll", "BWAPIVersion": "BWAPI_412", "ClientRequirements": [{"Property": "GPU"}]}
    ],
    
    "maps": 
    [
        "maps/aiide/(2)Benzene.scx",
        "maps/aiide/(2)Destination.scx"
    ],
    
    "gamesListFile"           : "games.txt",
    "resultsFile"             : "results.txt",
    "detailedResults"         : false,
    "serverPort"              : 1337,
    "clearResults"            : "ask",
    "startGamesSimultaneously": false,
    "tournamentType"          : "AllVsAll",
    "lobbyGameSpeed"          : "Normal",
    "enableBotFileIO"         : true,
    "ladderMode"              : false,
    "excludeFromResults"      : ["ExampleBot"],
    
    "tournamentModuleSettings":
    {
        "localSpeed"    : 0,
        "frameSkip"     : 256,
        "gameFrameLimit": 85714,
        "timeoutLimits" :
        [
            {"timeInMS" : 55,    "frameCount": 320},
            {"timeInMS" : 1000,  "frameCount": 10},
            {"timeInMS" : 10000, "frameCount": 1}
        ],
        "drawBotNames"      : true,
        "drawTournamentInfo": true,
        "drawUnitInfo"      : true    
    }
}
```
