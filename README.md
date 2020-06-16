# Pull the pitcher



#### [Documentation](https://collinprather.github.io/pull-the-pitcher/)

> Predicting when MLB managers in the AL will pull their starting pitchers.

## Installation

```shell
$ pip install pull-the-pitcher
```

## How to get the data

The `ptp` library comes with two main command-line utilites. After you install `ptp`, these should be directly available to you at the command-line, assuming you're in the environment that `ptp` was installed in.

### Storing data in a `sqlite3` db

The first command-line utility is `query_statcast`, which invokes `pybaseball`'s [`statcast()`](https://github.com/jldbc/pybaseball#statcast-pull-advanced-metrics-from-major-league-baseballs-statcast-system) function to retrieve pitch-level data from statcast. This data will then be stored in a [`sqlite3` db file](https://www.sqlite.org/fileformat.html). Here's an example of how you could use it.

```shell
$ query_statcast --start_dt 2019-05-07 --end_dt 2019-06-09 --output_type db --output_path /tmp
This is a large query, it may take a moment to complete
Completed sub-query from 2019-05-07 to 2019-05-12
Completed sub-query from 2019-05-13 to 2019-05-18
Completed sub-query from 2019-05-19 to 2019-05-24
Completed sub-query from 2019-05-25 to 2019-05-30
Completed sub-query from 2019-05-31 to 2019-06-05
Completed sub-query from 2019-06-06 to 2019-06-09
```

### Preparing data for modeling

The next command-line utility is `prep_data_for_modeling`, which pulls data from the database created in the previous command, then performs feature engineering and various aggregations to yield clean, at-bat level data amenable to a machine learning model. Here's an example of how you might use it.

```shell
$ prep_data_for_modeling --db_path /tmp/statcast_pitches.db --train_test_split_by start --output_path /tmp/
querying db at /tmp/statcast_pitches.db now.
In this dataset, there are 457 total games.
There are 63 'openers' in the dataset.
There are 851 total eligible game-pitcher combinations in this dataset.
Just processed 0th start.
Just processed 100th start.
Just processed 200th start.
Just processed 300th start.
Just processed 400th start.
Just processed 500th start.
Just processed 600th start.
Just processed 700th start.
Just processed 800th start.
There are 91 unique pitcher's in this dataset
['2019'] data ready for modeling and saved at /tmp/.
```

## FAQ

* **Should any of the data be considered "uncensored"?**

    - The great thing about baseball data is that it is comprehensive, clean, and public! So, **no, none of the data is "censored"** in the survival analysis sense. We know the exact at bat at which every pitcher was removed from the game.


* **If none of the data is uncensored, why are you using survival analysis techniques?**

    - Well, the short answer is that they perform the best. Much of survival analysis is dedicated to modeling with [both censored and uncensored data](https://square.github.io/pysurvival/intro.html). Since none of our data is cenored, we have free reign to leverage any predictive modeling technique under the sun. Here, however, the process of predicting when a pitcher will be removed from a game fits very nicely in a time-to-event modeling framework, which survival analysis techniques are designed to handle.


* **How does this approach compare to traditional survival analysis?**

    - [Traditional survival analysis](http://www.sthda.com/english/wiki/cox-proportional-hazards-model) is typically framed as a regression problem, which involves _regressing_ the estimated units of time until the event of interest occurs. Alternatively, the approach we employ is framed as a classification problem, and involves predicting the _probability_ that the event of interest (pitcher removed from the game) occurs at every unit of time (at bat). 
        - While this neural network, classification-esque approach is non-traditional, it is not unheard of, as seen [here](https://www.stats.ox.ac.uk/pub/bdr/NNSM.pdf) and [here](http://pcwww.liv.ac.uk/~afgt/eleuteri_lyon07.pdf).
        
        
* **How is this Deep, Recurrent Survival Analysis model different from a traditional LSTM?**
    
    1. Like other recurrent neural networks, our model predicts the conditional probability that a pitcher was pulled after each at-bat (conditioned on the game that has occurred up to that point). The novelty here occurs in the way that the model "estimates the survival rate through the probability chain rule, which captures the sequential dependency patterns between neighboring at-bats and back-propagates the gradient more efficiently." (quote from page 2 of [the original paper](https://arxiv.org/pdf/1809.02403.pdf)).
        
    2. This notion of estimation of the survival rate through the probability chain rule is further enforced by the use of the [event time](https://collinprather.github.io/drsa/functions/#Event-Time-Loss) and the [event rate](https://collinprather.github.io/drsa/functions/#Event-Rate-Loss) loss functions. Notice that while our targets are binary, _we are not using traditional [log loss](http://wiki.fast.ai/index.php/Log_Loss#Binary_Classification) to train this model_.
