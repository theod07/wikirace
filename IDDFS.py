import requests
import time
import json
import sys

def get_title(wiki_url):
    """
    Return article's Wikipedia title.
    INPUT:
        wiki_url -- string url of article.
    OUTPUT:
        title -- string title of article.
    """
    title = wiki_url.split('/wiki/')[-1]
    return title


def get_url(title):
    """
    Return article's Wikipedia URL.
    INPUT:
        title -- string title of article.
    OUTPUT:
        fullurl -- string url of article.
    """
    URL = 'http://en.wikipedia.org/w/api.php'
    params = {
    'action':'query',
    'prop':'info',
    'inprop':'url',
    'format':'json'
    }
    params['titles'] = title
    r = requests.get(URL, params)
    j = json.loads(r.content)
    pageid = j['query']['pages'].keys()[0]
    return j['query']['pages'][pageid]['fullurl']


def get_children(title):
    """
    Return a set of article titles that appear in body of article.
    INPUT:
        title -- string title of article.
    OUTPUT:
        titles -- set of article titles
    """
    URL = 'http://en.wikipedia.org/w/api.php'
    params = {
    'action':'query',
    'prop':'links',
    'pllimit':'max',
    'format':'json',
    }
    params['titles'] = title
    r = requests.get(URL, params)
    j = json.loads(r.content)

    if len(j['query']['pages']) == 1:
        pageid = j['query']['pages'].keys()[0]
    else:
        print "len(j['query']['pages']) != 1"

    try:
        links = j['query']['pages'][pageid]['links']
        titles = set(l['title'] for l in links)
    except KeyError as ke:
        return set()

    while 'continue' in j:
        params['plcontinue'] = j['continue']['plcontinue']
        r = requests.get(URL, params)
        j = json.loads(r.content)
        links = j['query']['pages'][pageid]['links']
        titles = titles.union(set(l['title'] for l in links))

    return titles


def get_parents(title):
    """
    Return a set of article titles that link to this article.
    """
    pass


def IDDFS(start_url, end_url):
    """
    Iteratively calls function DepthLimitedSearch (DLS) to find a path while
    incrementing the allowed depth. Return a list of article titles that connect
    from a starting article to an ending article.
    Assumes that articles are separated by roughly "Six Degrees" with 1.5x
    margin.

    INPUT:
        start_url -- string url of starting article.
    OUTPUT:
        end_url -- string url of ending article.

    Reference:
    https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
    """
    start_title = get_title(start_url)
    end_title = get_title(end_url)
    # Assume "Six Degrees" of separation * 1.5x margin
    for depth in xrange(9):
        print 'depth : ', depth
        route = DLS(start_title, end_title, depth)
        if route:
            return route
    return 'Unable to find route up to depth=9'


def DLS(start, end, depth):
    """
    Depth Limited Search is an implementation of Depth First Search with a
    limited depth. Continually search through child nodes in a last-in-first-out
    (LIFO) order until the desired end node is found.

    INPUT:
        start -- string title of starting article
        end -- string title of ending article
        depth -- integer depth to limit Search
    OUTPUT:
        path -- list of titles in sequence, when path is found
        OR
        None -- when path is not found

    Reference:
        https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search#Algorithm
    """
    if start == end:
        return [start]

    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()

        child_nodes = get_children(vertex)
        if end in child_nodes:
            return path + [end]

        for next in child_nodes - set(path):
            if next == end:
                return path + [next]
            elif len(path) < depth:
                stack.append((next, path + [next]))
    return


def path_titles_to_urls(titles):
    """
    INPUT:
        titles -- list of Wikipedia article titles
    OUTPUT:
        urls -- list of Wikipedia article URLs
    """
    urls = [get_url(title) for title in titles]
    return urls


def test_cases():
    """
    Test out some start and end_title articles.

    """
    start = 'https://en.wikipedia.org/wiki/Malaria'
    end0 =  'https://en.wikipedia.org/wiki/Malaria'
    end1 = 'https://en.wikipedia.org/wiki/Agriculture'
    end2 = 'https://en.wikipedia.org/wiki/M._King_Hubbert'
    end3 = 'https://en.wikipedia.org/wiki/Geophysics'

    if False:
        print 'This search should require depth=0'
        tstart = time.time()
        print IDDFS(start, end0)
        print 'tdelta : ', time.time() - tstart

    if True:
        print 'This search should require depth=1'
        tstart = time.time()
        print IDDFS(start, end1)
        print 'tdelta : ', time.time() - tstart

    if False:
        print 'This search should require depth=2'
        tstart = time.time()
        print IDDFS(start, end2)
        print 'tdelta : ', time.time() - tstart

    if False:
        print 'This search should require depth=3'
        tstart = time.time()
        print IDDFS(start, end3)
        print 'tdelta : ', time.time() - tstart


def main():
    """

    """
    json_obj = json.loads(sys.argv[1])
    path = IDDFS(json_obj['start'], json_obj['end'])
    json_obj['path'] = [get_url(p) for p in path]
    return json_obj


if __name__ == '__main__':

    print main()
    # test_cases()
