from wiki_node import wiki_node as wnode
from collections import Counter
import itertools
import time
import json
import sys

def IDDFS(start, end):
    """
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    route = Counter()
    route[start] += len(route)
    for depth in itertools.count():
        found = DLS(c, end, depth)

        if found:
            return found

def DLS(route, end, depth):
    """
    route is a counter object to take advantage of the constant lookup time of a dictionary, as well as capability to quickly search for max index of the route.
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    if depth == 0:
        return

    current = route.most_common(1)[0][0]
    if current == end:
        return route

    for child in wnode(current).child_nodes:
        if not child in route:
            route[child] += len(route)
            next_route = DLS(route, end, depth-1)
            if next_route:
                return next_route

    if depth < 0:
        return 'Depth cannot be negative.'

    return

def test_cases():
    """
    Test out some start and end articles.
    This search should require depth=0
    Sample output:
        depth:  0
        depth:  1
        current == end
        ['https://en.wikipedia.org/wiki/Malaria']
        tdelta :  7.10487365723e-05
        This search should require depth=1
        depth:  0
        depth:  1
        depth:  2
        current == end
        ['https://en.wikipedia.org/wiki/Malaria', 'https://en.wikipedia.org/wiki/Agriculture']
        tdelta :  74.5454380512
        This search should require depth=2
        depth:  0
        depth:  1
        depth:  2
        depth:  3
    """
    start = 'https://en.wikipedia.org/wiki/Malaria'
    end0 =  'https://en.wikipedia.org/wiki/Malaria'
    end1 = 'https://en.wikipedia.org/wiki/Agriculture'
    end2 = 'https://en.wikipedia.org/wiki/M._King_Hubbert'
    end3 = 'https://en.wikipedia.org/wiki/Geophysics'

    if True:
        print 'This search should require depth=0'
        tstart = time.time()
        print IDDFS(start, end0)
        print 'tdelta : ', time.time() - tstart

    if True:
        print 'This search should require depth=1'
        tstart = time.time()
        print IDDFS(start, end1)
        print 'tdelta : ', time.time() - tstart

    if True:
        print 'This search should require depth=2'
        tstart = time.time()
        print IDDFS(start, end2)
        print 'tdelta : ', time.time() - tstart

    if True:
        print 'This search should require depth=3'
        tstart = time.time()
        print IDDFS(start, end3)
        print 'tdelta : ', time.time() - tstart

def main():
    json_obj = json.loads(sys.argv[1])
    path = IDDFS(json_obj['start'], json_obj['end'])
    json_obj['path'] = path
    return json_obj


if __name__ == '__main__':

    print main()
