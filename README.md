# Vote Predict App on Heroku

This project is to build a website application to predict which voters are likely to switch political parties. This app will help political parties to focus their campaign efforts. [The data]( https://www.voterstudygroup.org/publications/2016-elections/data) is a political survey that contains 8000 of records of answers to hundreds of questions. My trained model predicts the political party of a voter based on the answers to selected survey questions, and how likely the voter is going to switch the party. The web site link is [https://dataincubator-proj-voter.herokuapp.com/](https://dataincubator-proj-voter.herokuapp.com/)

## Prediction

A logistic regression model is trained to predict a voter's party from answers to selected survey questions. It outputs a table of inputs, the prediction of party, logistic probability, and the probabilities of switching. A voter is more republican if the logistic probability is more close to 1, and more democratic if the logistic probability is more close to 0. The probability of switching from either party is estimated by counting the fraction of switchers in the data that belong to the same party and has similar logistic probability. The metrics of training and test sets are shown as below:

classification report on training set:

|| precision | recall | f1-score | support |
| --- | --- | --- | --- | --- |
| 0 | 0.96 | 0.96 | 0.96 | 1024 |
| 1 | 0.96 | 0.96 | 0.96 | 1025 |
| avg / total | 0.96 | 0.96 | 0.96 | 2049 |


classification report on test set:

|| precision | recall | f1-score | support |
| --- | --- | --- | --- | --- |
| 0 | 0.95 | 0.96 | 0.96 | 2423 |
| 1 | 0.96 | 0.95 | 0.96 | 2358 |
| avg / total | 0.96 | 0.96 | 0.96 | 2049 |

And the [learning curves (accuracy)](images/DR_lc.png)

## Distribution by Features

This plots the counts of Republican vs Democrat in each category of selected features. It is to help finding interesting features that distinguish Republican and Democrat. For selected features, a plot is generated, each feature is shown in one color, and each circle correspond to one category within that feature. Features of which the data points align along the 45° line are not interesting, and features of which the data points fall close to x/y axis can help to distinguish between Republican and Democrat. 
