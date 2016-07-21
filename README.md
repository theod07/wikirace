# wikirace

### Problem Statement
Wikiracing is a game that people play on Wikipedia. Given a starting article and an ending article, the objective of a wikirace is to get from the starting article to the ending article by only clicking on links occurring in the main bodies of wikipedia articles (not including the side navigation bar or the category footer).

Write a wikiracing bot, which will take race specifications in the form of a JSON object:

```
{

    ''start'': ''<starting article>'',

    ''end'': ''<ending article>''

}
```

and which will return the results of the race in the form of a JSON object:

```
{
    ''start'': ''<starting article>'',
    ''end'': ''<ending article>'',
    ''path'': [
        ''<starting article>'',
        ''<article at step 1>'',
        ''<article at step 2>'',
        :
        :
        ''<article at step n-1>'',
        ''<ending article>''
    ]
}
```

Each article will be identified with a fully expanded URL. So, for example, the Wikipedia article about “World War II” will be represented by the URL https://en.wikipedia.org/wiki/World_War_II
