#!/usr/bin/env python3

# launch bwheadless and chaoslauncher from here!

import argparse

parser = argparse.ArgumentParser()

parser.add_argument()
parser.add_argument()

args = parser.parse_args()

```
wine bwheadless.exe -e /opt/StarCraft/StarCraft.exe\
 -l /opt/StarCraft/bwapi-data/BWAPI.dll --host\
 --name blueberry --game blueberry --race T\
 --map maps/TorchUp/\(4\)FightingSpirit1.3.scx&\
wine Chaoslauncher/Chaoslauncher.exe
```
