
import argparse
import torchcraft as tc
import torchcraft.Constants as tcc

parser = argparse.ArgumentParser(
    description='Plays simple micro battles with an attack closest heuristic')
parser.add_argument('-t',
                    '--hostname',
                    type=str,
                    default='127.0.0.1',
                    help='Hostname where SC is running')
parser.add_argument('-p', '--port', default=11111,
                    help="Port to use")

args = parser.parse_args()


def get_closest(x, y, units):
    dist = float('inf')
    u = None
    for unit in units:
        d = (unit.x - x)**2 + (unit.y - y)**2
        if d < dist:
            dist = d
            u = unit
    return u


skip_frames = 7


while True:
    print("")
    print("CTRL-C to stop")
    print("")
    loop = 0
    client = tc.Client()
    client.connect(args.hostname, args.port)
    state = client.init(micro_battles=False)
    for pid, player in state.player_info.items():
        print("player {} named {} is {}".format(
            player.id, player.name,
            tc.Constants.races._dict[player.race]))
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
        client.send(actions)
    client.close()
