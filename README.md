# wikirace

### Instructions
This installation assumes that you have Python2.7 `pip` installed on your machine.
Python dependencies are listed in requirements.txt.
Good practice to create a separate environment to install the required dependencies to avoid potential conflicts across different projects. `virtualenv` and Anaconda (`conda`) are both environment managers for Python, but have been known to conflict with each other.

To upgrade `pip` and install requirements:
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

The first ideas that came to mind when traversing through this graph were to use Breadth-First Search (BFS) or Depth-First Search (DFS). Each method has its benefits and drawbacks, mentioned below. The final implementation here uses a hybrid of the two techniques: [Iterative Deepening DFS](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search).

#### Breadth-First Search
###### Pros
* Reason1
* Reason2

###### Cons
* Reason1
* Reason2

#### Depth-First Search
###### Pros
* Reason1
* Reason2

###### Cons
* Reason1
* Reason2

#### Iterative Deepening DFS
###### Pros
* Reason1
* Reason2

###### Cons
* Reason1
* Reason2

### Improvements
