# Put effort into a good set of tools
# which allow to build custom solutions.


def get_closest(x, y, units):
    dist = float('inf')
    u = None
    for unit in units:
        d = (unit.x - x)**2 + (unit.y - y)**2
        if d < dist:
            dist = d
            u = unit
    return u

def check_supported_maps(name):
    '''
    '''
    pass
