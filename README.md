# starcraft-scif
This repository prepares StarCraft: Brood War bots running inside a SIF (Singularity Image Format) a single executable file based container image, auditable, secure, and easy to move using existing data mobility paradigms.

It can download and launch [SSCAIT](http://sscaitournament.com/) 32bit C++, Java bots and native 64bit Linux® bots that use BWAPI `4.1.2, 4.2.0, 4.4.0` to communicate with the game.

## Headless play

Launch headless play of [Ophelia](https://liquipedia.net/starcraft/Ophelia) and [Blueberry](https://liquipedia.net/starcraft/Blueberry) on current maps.
```
    $ pkg -u starcraft run -x "Ophelia Blueberry"
```

## Development

### Add your own bot

Place your bot to `--bot_dir` directory. Some of these are inspired by [SSCAIT rules](http://sscaitournament.com/index.php?action=rules).

Use this structure:

- **/AI/** - put your bot binaries here.

- **/read/** - folder where you can put your config files, initial opponent modelling etc.

  It's contents may be overwritten. After running games contents of the write folder can be copied here, see below.

- **/write/** - folder where bot can write.

    Note that `bw` creates subdirectories in write folder, for each game it's own. The contents of the *write/GAME_xxx* folder will be copied to the *read* folder.

- **/bot.json** - bot configuration. Minimal config is following:

        {
          "name": "Perran",
          "race": "Terran",
          "type": "Python",
        }

    `name` must match `[a-zA-Z0-9_][a-zA-Z0-9_. -]{0,40}`

    `race` can be one of {`Terran`, `Zerg`, `Protoss`, `Random`}

    `type` can be one of {`Java`, `AI_MODULE`, `EXE`, `Python`, `LuaJIT`, `LFE`}
