# Learning to use the TochCraft Python 3 client!

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


bot = {'name': 'Blueberry'}

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
refineries = 0


# TODO: command_unit

# TODO: log state and compare the javascript data structure

while True:
    print("CTRL-C to stop")
    loop = 0
    client = tc.Client()
    client.connect('127.0.0.1', 11111)
    state = client.init(micro_battles=True)
    # Initial setup
    client.send([
        [tcc.set_speed, 0],
        [tcc.set_gui, 1],
        [tcc.set_cmd_optim, 1],
    ])
    while not state.game_ended:
        loop += 1
        state = client.recv()
        for pid, player in state.player_info.items():
            if bot['name'] == player.name:
                bot['id'] = state.player_id
                bot['neutral'] = state.neutral_id
                bot['race'] = tc.Constants.races._dict[player.race]
            else:
                bot['enemy'] = (player.id if player.name != 'Neutral' else False)
        workers = []
        actions = []
        if state.game_ended:
            break
        else:
            units = state.units[bot['id']]
            neutral = state.units[bot['neutral']]
            enemy = state.units[bot['enemy']]
            if state.battle_frame_count % skip_frames == 0:
                used_psi = state.frame.resources[bot['id']].used_psi
                total_psi = state.frame.resources[bot['id']].total_psi
                if used_psi != total_psi:
                    building_supply = False
                # ok go!
                for unit in units:
                    if tcc.isbuilding(unit.type)\
                     and tc.Constants.unittypes._dict[unit.type]\
                     == 'Terran_Command_Center':
                        # train worker only if not producing(?)
                        if not producing\
                                and state.frame.resources[bot['id']].ore >= 50\
                                and state.frame.resources[bot['id']].used_psi\
                                != state.frame.resources[bot['id']].total_psi:
                            # Target, x, y are all 0
                            actions.append([
                                tcc.command_unit_protected,
                                unit.id,
                                tcc.unitcommandtypes.Train,
                                0,
                                0,
                                0,
                                tc.Constants.unittypes.Terran_SCV,
                            ])
                            # to train a unit you MUST input into "extra" field
                            producing = True
                    if tcc.isworker(unit.type):
                        workers.append(unit.id)
                        # tests gathering
                        print('unit order: {}'.format(unit.orders))
                        print(tcc.unitcommandtypes.Gather)
                        print(tcc.unitcommandtypes.Build)
                        print(tcc.unitcommandtypes.Right_Click_Position)
                        print(tcc.command2order[tcc.unitcommandtypes.Gather])
                        print(tcc.command2order[tcc.unitcommandtypes.Build])
                        print(tcc.command2order[tcc.unitcommandtypes.Right_Click_Position])
                        # lolz
                        print(neutral)
                        # target = get_closest(unit.x, unit.y, state.frame.units_neutral, [])
                    else:
                        target = get_closest(unit.x, unit.y, enemy)
                        if target is not None:
                            actions.append([
                                tcc.command_unit_protected,
                                unit.id,
                                tcc.unitcommandtypes.Attack_Unit,
                                target.id,
                            ])
                print(workers)
        print("Sending actions: {}".format(str(actions)))
        print(state.map_name)
        print(state.frame.resources[bot['id']].gas)
        client.send(actions)
    client.close()
