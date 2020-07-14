#!/usr/bin/env python3

# Run bwheadless.exe and Chaoslauncher.exe from here!

import argparse
import os

parser = argparse.ArgumentParser(description='host a game with bwheadless')

parser.add_argument('-p', '--path',
                    type=str,
                    default='/opt/StarCraft/',
                    help='StarCraft path')
parser.add_argument('-b', '--bot',
                    type=str,
                    default='blueberry')
parser.add_argument('-r', '--race',
                    type=str,
                    default='Terran')
parser.add_argument('-m', '--map',
                    type=str,
                    default='\(4\)FightingSpirit1.3.scx')

args = parser.parse_args()

execute = '''
wine bwheadless.exe -e {0}StarCraft.exe\
 -l {0}bwapi-data/BWAPI.dll --host\
 --name {1} --game {1} --race {2}\
 --map maps/TorchUp/{3}&\
wine Chaoslauncher/Chaoslauncher.exe
'''.format(args.path, args.bot, args.race[:1], args.map)

os.chdir(args.path)
os.popen(execute).read()
