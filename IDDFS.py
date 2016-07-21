from wiki_node import wiki_node as wnode
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
    for depth in itertools.count():
        found = DLS([start], end, depth)

        if found:
            return found

def DLS(route, end, depth):
    """
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    if depth == 0:
        return

    current = route[-1]
    if current == end:
        return route

    for child in wnode(current).child_nodes:
        if not child in route:
            next_route = DLS(route + [child], end, depth-1)
            if next_route:
                return next_route

    if depth < 0:
        return 'Depth cannot be negative.'


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

if __name__ == '__main__':

    print 'This is the name of the script: ', sys.argv[0]
    print 'Number of arguments: ', len(sys.argv)

    json_obj = json.loads(sys.argv[1])
    print IDDFS(json_obj['start'], json_obj['end'])
