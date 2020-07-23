# learning to use the tochcraft python client!

import torchcraft as tc
import torchcraft.Constants as tcc

def get_closest(x, y, units):
    dist = float('inf')
    u = None
    for unit in units:
        d = (unit.x - x)**2 + (unit.y - y)**2
        if d < dist:
            dist = d
            u = unit
    return u


bot = {'name': 'blueberry'}

skip_frames = 7

# check past
built_barracks = 0

# active doing
building_supply = False
producing = False

# units
units = None
workers = 0

# buildings
supply_depots = 0
barracks = 0
command_centers = 0
factories = 0
starports = 0
turrets = 0
engineering_bay = 0
academy = 0
armory = 0
bunkers = 0
refineries = 0


# TODO: state.resources_myself.used_psi, state.resources_myself.total_psi

# TODO: tc:filter_type, tc:isbuilding, state.resources_myself.ore

# TODO: tc:isworker (?)

# TODO: explore whatever is in tc! where are our functions!

# TODO: pretty print the state and compare with the javascript data structure

# and now for something completely different!

# TODO: state.resources_myself.used_psi, state.resources_myself.total_psi

# TODO: filter_type, state.units_myself, isbuilding state.resources_myself.ore

# TODO:isworker, tc.command2order tc.unitcommandtypes, tc.command_unit

while True:
    print("CTRL-C to stop")
    loop = 0
    client = tc.Client()
    client.connect('127.0.0.1', 11111)
    state = client.init(micro_battles=True)
    for pid, player in state.player_info.items():
        print("player {} named {} is {}".format(
            player.id, player.name,
            tc.Constants.races._dict[player.race]))
        if bot['name'] == player.name:
            bot['id'] = player.id
            bot['race'] = tc.Constants.races._dict[player.race]
    # Initial setup
    client.send([
        [tcc.set_speed, 0],
        [tcc.set_gui, 1],
        [tcc.set_cmd_optim, 1],
    ])
    while not state.game_ended:
        loop += 1
        state = client.recv()
        actions = []
        if state.game_ended:
            break
        else:
            units = state.units[0]
            enemy = state.units[1]
            if state.battle_frame_count % skip_frames == 0:
                for unit in units:
                    target = get_closest(unit.x, unit.y, enemy)
                    if target is not None:
                        actions.append([
                            tcc.command_unit_protected,
                            unit.id,
                            tcc.unitcommandtypes.Attack_Unit,
                            target.id,
                        ])
        print("Sending actions: {}".format(str(actions)))
        # print(state.map_name)
        print(state.frame.resources[bot['id']].ore)
        client.send(actions)
    client.close()
