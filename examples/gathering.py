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


bot = {'id': 0, 'name': 'Blueberry'}

skip_frames = 7

# check past
built_barracks = 0

# active doing
building_supply = False
# producing what friend?
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


# TODO: isworker, filter_type, isbuilding

# TODO: command2order unitcommandtypes, command_unit

# TODO: pretty print the state and compare with the javascript data structure

while True:
    print("CTRL-C to stop")
    loop = 0
    client = tc.Client()
    client.connect('127.0.0.1', 11111)
    state = client.init(micro_battles=True)
    for pid, player in state.player_info.items():
        if bot['name'] == player.name:
            bot['id'] = player.id
            bot['race'] = tc.Constants.races._dict[player.race]
        else:
            bot['enemy'] = (player.id if player.name != 'Neutral' else False)
    # Initial setup
    client.send([
        [tcc.set_speed, 0],
        [tcc.set_gui, 1],
        [tcc.set_cmd_optim, 1],
    ])
    while not state.game_ended:
        loop += 1
        state = client.recv()
        workers = []
        actions = []
        if state.game_ended:
            break
        else:
            units = state.units[bot['id']]
            enemy = state.units[bot['enemy']]
            if state.battle_frame_count % skip_frames == 0:

                used_psi = state.frame.resources[bot['id']].used_psi
                total_psi = state.frame.resources[bot['id']].total_psi

                if used_psi != total_psi:
                    building_supply = False

                # ok go!
                for unit in units:

                    if tc.Constants.unittypes._dict[unit.type] == 'Terran_SCV':
                        workers.append(unit.id)

                    # check if building do [a, b, c] if worker do [x, y, z]
                    if tc.Constants.unittypes._dict[unit.type]\
                            == 'Terran_Command_Center':

                        if not producing\
                                and state.frame.resources[bot['id']].ore >= 50\
                                and state.frame.resources[bot['id']].used_psi\
                                != state.frame.resources[bot['id']].total_psi:
                            print('mini mini mini')

                    print(tc.Constants.unittypes._dict.get(unit.type))

                    target = get_closest(unit.x, unit.y, enemy)
                    if target is not None:
                        actions.append([
                            tcc.command_unit_protected,
                            unit.id,
                            tcc.unitcommandtypes.Attack_Unit,
                            target.id,
                        ])

                    # else and just else... gather some resources? wtf xD

                print(workers)

        print("Sending actions: {}".format(str(actions)))
        print(state.map_name)
        print(state.map_size)
        # print(state.start_locations)
        print(state.frame.resources[bot['id']].ore)
        print(state.frame.resources[bot['id']].gas)
        # print(state.frame.resources[bot['id']].used_psi)
        # print(state.frame.resources[bot['id']].total_psi)
        client.send(actions)
    client.close()
