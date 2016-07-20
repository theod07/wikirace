from wiki_node import wiki_node as wnode

def IDDFS(root):
    """
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    for depth in xrange(2):
        found = DLS(root, depth)
        print 'IDDFS, found     : ', found
        print 'IDDFS, found.url : ', found.url
        if found.url == 'https://en.wikipedia.org/wiki/Tree_traversal':
            print 'FOUND IT'
            print found
            return found


def DLS(node, depth):
    """
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    # print 'depth   : ', depth
    # print 'node.url: ', node.url
    if depth == 0:
        # print 'depth = 0'
        print 'depth = 0'
        print node.url
        return node
    elif depth > 0:
        print 'depth > 0'
        print 'num_child_nodes : ', len(node.child_nodes)
        for child in node.child_nodes[:10]:
            child_node = wnode(child)
            found = DLS(child_node, depth-1)
            return found
    else:
        print 'Depth of search cannot be negative.'



if __name__ == '__main__':
    start_node = wnode('https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search')

    # print DLS(start_node, 2)
    IDDFS(start_node)
