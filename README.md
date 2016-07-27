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

We chose to query Wikipedia's mediawiki api using python's `requests` library, which allows us to get the articles that are linked from a given page.

The IDDFS function takes in two strings, start_url and end_url, which are the URLs of the articles, and calls the Depht-Limited Search (DLS) function at each incremental increase in depth. In theory we could increment forever until we find a search, but chose to limit the depth to nine by assuming articles are connected by 6 degrees of separation with a margin of 1.5. Once DLS finds the end node, IDDFS returns the traversed path.

The DLS function takes in three arguments: start (a string of the article title), end (a string of the article title), and depth (an integer limiting the depth of search). DLS continually explores child nodes in a Last-In-First-Out (LIFO) order. At each new node, the child nodes are returned in a set and we check whether the end-node appears in the set of child nodes. This is beneficial because checking whether an element is in a set is a fast operation.


### Improvements
While Iterative-deepening DFS is an improvement over BFS and DFS, it can be improved if we search in both directions at the same time. The search in the opposite direction would be symmetric where we would explore the parent nodes for a given article and store them in a set. Consider searching in the forward direction when depth is even and searching in the reverse direction when depth is odd until a path is found. The benefit of this bi-directional search is that the rate that we discover new nodes to explore is significantly less than in the one-directional search (assuming that the number of links on a page is constant).

The bi-directional search will decrease the amount of computation required, but will require extra functionality: we would need a way to check whether the paths that we have explored in both directions have met each other. One idea would be to treat the fringe nodes as two sets (parents and children). An "AND" operation on the two sets at the end of each iteration would identify any nodes that connect two paths.

The function `get_children()` includes a try/except handle `KeyError`s when they occur. Future improvements to this implementation may benefit from understanding the reason for `KeyError` and handle the exception more intelligently/robustly.

Function `get_children()` is called repeatedly throughout this implementation, one article at a time. Future improvements may consider querying the API for multiple articles at a time and caching the results, which may improve performance as well as reduce loading to API server. Further testing required.
