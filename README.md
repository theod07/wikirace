# wikirace

### Instructions
This installation assumes that you have Python2.7 `pip` installed on your machine.
Python dependencies are listed in requirements.txt.
It's good practice to create a separate environment to install the required dependencies to avoid potential conflicts across different projects. `virtualenv` and Anaconda (`conda`) are both environment managers for Python, but have been known to conflict with each other. If you're not already using Anaconda, you'll probably want to use `virtualenv` because Anaconda is a relatively large package -- it installs many of Python's scientific computing libraries.

Once you're ready to go, you can upgrade `pip` and install requirements:
```
pip install --upgrade pip
pip install -r requirements.txt
```

You can run the script by entering `./wikirace` into the command line followed by the `json` object with appropriate URLs to starting and ending Wikipedia articles.
```
$ ./wikirace '{
  "start":"https://en.wikipedia.org/wiki/Malaria",
  "end":"https://en.wikipedia.org/wiki/Agriculture"
  }'
```

### Problem Statement
Wikiracing is a game that people play on Wikipedia. Given a starting article and an ending article, the objective of a wikirace is to get from the starting article to the ending article by only clicking on links occurring in the main bodies of wikipedia articles (not including the side navigation bar or the category footer).

Write a wikiracing bot, which will take race specifications in the form of a JSON object:

```
{
    "start": "<starting article>",
    "end": "<ending article>"
}
```

and which will return the results of the race in the form of a JSON object:

```
{
    "start": "<starting article>",
    "end": "<ending article>",
    "path": [
        "<starting article>",
        "<article at step 1>",
        "<article at step 2>",
        :
        :
        "<article at step n-1>",
        "<ending article>"
    ]
}
```

Each article will be identified with a fully expanded URL. So, for example, the Wikipedia article about “World War II” will be represented by the URL https://en.wikipedia.org/wiki/World_War_II

### Methodology
Wikirace can be viewed as a search problem where we're looking for the ending article and keeping track of the articles we see along the route to reach it. Naturally, we can view the space of Wikipedia as a collection of nodes and edges, where each Wikipedia article is a node and each link in the article body is a directed edge (from the current article to the target article).

The first ideas that came to mind when traversing through this graph were to use [Breadth-First Search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search) or [Depth-First Search (DFS)](https://en.wikipedia.org/wiki/Depth-first_search). Each method has its benefits and drawbacks. The final implementation here uses a hybrid of the two techniques: [Iterative Deepening DFS](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search).

In general, the decision to use BFS or DFS to traverse a graph should take into consideration the structure of the data. DFS is advantageous when the each node has few child nodes and the start node is far from the end node. BFS is advantageous when each node has many child nodes and the start node is near to the end node. All else equal, BFS is guaranteed to find the shortest path and DFS does not (if the path exists).

In Iterative Deepening DFS, we DFS to a set depth and increment the depth at each step. This guarantees that the shortest path will be found (if it exists).

We created a class called `wiki_node` with two attributes:
1. url - the url for the given Wikipedia article
2. child_nodes - a list of url links contained in the article body

The article's HTML is retrieved through Python's `requests` library and parsed using `BeautifulSoup`'s `html.parser`. Links on the page were by filtering out tags that began with `/wiki/`. Additionally, we filtered out any links that contain `/wiki/File:` and `/wiki/Special:` because they do not add valuable nodes to our graph.

One article on Wikipedia may have duplicate links that point to the same page. To avoid keeping track of any duplicated pages, we store the href links (`child_nodes`) as a set. This has the combined benefit of constant time to look-up (check for inclusion) as well as constant time to add a new item. Note: a set does not necessarily maintain order of the input.

The IDDFS function takes in two strings, start and end, which are the URLs of the articles, and calls the Depht-Limited Search (DLS) function for incremental increase in depth. Once DLS finds the end node, IDDFS returns the traversed path.

The DLS function takes in three arguments: route (a Counter object), end (a string), and depth (an integer). It recursively calls DLS, decrementing depth each time and returns nothing until the current node matches the end node.

Route is stored as a Counter object rather than a for its constant look up time. If a node has already appeared in our current route, we want to avoid exploring it again. The Counter's keys are the nodes and the values are the indices where the node appears in the route. Calling Counter's method `.most_common()` efficiently sorts the keys by value to reconstruct the route's correct sequence.


### Improvements
While this implementation will find a shortest path, it is impractical to run for two arbitrary start/end articles with unknown depth because of the time required to solve. To improve this, consider parallelizing the search process. We could try to multithread this on a single machine, but there may be rate limits imposed on sending requests to Wikipedia. We could consider introducing some stop time in between requests to Wikipedia as a workaround or include a try/except condition to handle any bad responses from Wikipedia. We could try any bad responses at a later time.

Rather than running the risk of being blocked from Wikipedia from a single IP, it would be most beneficial to perform a distributed parallelized search if possible, where one machine/process searches for child nodes of itself and farms the search for each child node to separate machines/processes.

We've also assumed that the input will have valid URLs for Wikipedia articles. To make this more robust, consider including a helper function which validates each URL and/or website. Additionally, we have chosen to filter out href links that look like `/wiki/File:` and `/wiki/Special:` because they lead to pages that do not help our search. We can improve the implementation by finding other URLs that systematically do not add value to the search.
