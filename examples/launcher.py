#!/usr/bin/env python3

# Run bwheadless.exe and Chaoslauncher.exe from here!

import argparse

parser = argparse.ArgumentParser(descroption='host a local pc game with bwheadless')

parser.add_argument('-p', '--path', type='str', default='/opt/StarCraft/', help='StarCraft path')
parser.add_argument('-b', '--bot', type='str', default='blueberry')
parser.add_argument('-r', '--race', type='str', default='Terran')
parser.add_argument('-m', '--map', type='str', default='\(4\)FightingSpirit1.3.scx')

args = parser.parse_args()

```
wine bwheadless.exe -e /opt/StarCraft/StarCraft.exe\
 -l /opt/StarCraft/bwapi-data/BWAPI.dll --host\
 --name blueberry --game blueberry --race T\
 --map maps/TorchUp/\(4\)FightingSpirit1.3.scx&\
wine Chaoslauncher/Chaoslauncher.exe
```
