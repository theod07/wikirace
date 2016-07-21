from wiki_node import wiki_node as wnode
import itertools
import time

def IDDFS(start, end):
    """
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    for depth in itertools.count():
        print 'depth: ', depth
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
        print 'current == end'
        return route

    for child in wnode(current).child_nodes:
        if not child in route:
            next_route = DLS(route + [child], end, depth-1)
            if next_route:
                return next_route

    if depth < 0:
        return 'Depth cannot be negative.'


if __name__ == '__main__':
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

#
# In [35]: run IDDFS.py
# depth:  0
# depth:  1
# depth:  2
# current == end
# ['https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search', 'https://en.wikipedia.org/wiki/Time_complexity']
# tdelta1 :  16.2023248672
# depth:  0
# depth:  1
# depth:  2
# depth:  3
# current == end
# ['https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search', 'https://en.wikipedia.org/wiki/Backtracking', 'https://en.wikipedia.org/wiki/Algorithm']
# tdelta2 :  271.779721022
