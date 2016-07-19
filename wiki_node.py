from bs4 import BeautifulSoup
import requests

class wiki_node(object):
    """
    This wiki_node represents a single article on Wikipedia. An article
    typically contains links to other articles on Wikipedia.
    It will have two attributes:
        self.url          :  string url
        self.child_nodes  :  list of strings, one url for each link
                             contained in the body of the Wikipedia article
    """
    def __init__(self, url):
        self.url = url
        self.child_nodes = self.get_child_nodes(url)

    def get_child_nodes(self, url):
        DOMAIN = 'https://en.wikipedia.org'
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        # we're ignoring any links that appear in side navigation bar
        # and category footer.
        divs = soup.find_all(id='mw-content-text')
        a_tags = divs[0].find_all('a')
        # notice that we're only interested in links that begin with '/wiki/'
        hrefs = [DOMAIN + tag['href'] for tag in a_tags if tag['href'].startswith('/wiki/')]
        return hrefs

if __name__ == '__main__':
    site = 'https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search'
    node = wiki_node(site)
    print 'node: ', node
    print 'node.url', node.url
    print 'node.child_nodes', node.child_nodes
