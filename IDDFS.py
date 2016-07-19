def IDDFS(root):
    """
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    for depth in xrange(3):
        found = DLS(start, depth)
        if found:
            return found


def DLS(node, depth):
    """
    DOCSTRING PLACEHOLDER
    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    if depth == 0:
        return node
    elif depth > 0:
        for child in node.child_nodes:
            found = DLS(child, depth-1)
            return found
    else:
        print 'Depth of search cannot be negative.'
    return


if __name__ == '__main__':
