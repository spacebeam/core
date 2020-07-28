# do what you can, what you want,
# what you must, feel the hunger inside,
# hold on to your trust!

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


# sinsemilla
bot = {'name': 'Blueberry'}

skip_frames = 7

building_refinery = False
gas_harvesting = []
producing = False

# units
units = None
workers = 0

# buildings
refinery = 0


# let's keep going..
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
                bot['enemy'] = (player.id if player.name != 'Neutral' else None)
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
                        # build refinery
                        if state.frame.resources[bot['id']].ore >= 100 and not building_refinery:
                            for nu in neutral:
                                if tcc.unittypes._dict[nu.type] == 'Resource_Vespene_Geyser':
                                    gas_harvesting.append(unit.id)
                                    actions.append([
                                        tcc.command_unit,
                                        unit.id,
                                        tcc.unitcommandtypes.Build,
                                        -1,
                                        nu.x - 8,
                                        nu.y - 4,
                                        tcc.unittypes.Terran_Refinery,
                                    ])
                            building_refinery = True
                        # tests gathering
                        for order in unit.orders:
                            if order.type not in tcc.command2order[tcc.unitcommandtypes.Gather]\
                             and order.type not in tcc.command2order[tcc.unitcommandtypes.Build]\
                             and order.type not in tcc.command2order[tcc.unitcommandtypes.Right_Click_Position]\
                             and not building_refinery:
                                if len(gas_harvesting) == 1:
                                    print('one or {}'.format(gas_harvesting[0]))
                                elif len(gas_harvesting) == 2:
                                    pass
                                elif len(gas_harvesting) == 3:
                                    pass
                                else:
                                    print('omfg {0}'.format(len(gas_harvesting)))
                                    target = get_closest(unit.x, unit.y, neutral)
                                    if target is not None:
                                        actions.append([
                                            tcc.command_unit_protected,
                                            unit.id,
                                            tcc.unitcommandtypes.Right_Click_Unit,
                                            target.id,
                                        ])
                            else:
                                print('wtf {}'.format(len(gas_harvesting)))
                        # we need to check the worker ids
                        # and put 3 of them, including the one that build the refinery
                        # into gas harvesting!
                    else:
                        target = get_closest(unit.x, unit.y, enemy)
                        if target is not None:
                            actions.append([
                                tcc.command_unit_protected,
                                unit.id,
                                tcc.unitcommandtypes.Attack_Unit,
                                target.id,
                            ])
                print(len(workers))
        # print("Sending actions: {}".format(str(actions)))
        client.send(actions)
    client.close()
