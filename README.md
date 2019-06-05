# RS-Pattern-Matching

## Using Machine Learning to Make Predictions on the Runescape Stock Market

### Introduction: 
#### RuneScape is an online fantasy MMORPG (Massively Multiplayer Online Role Playing Game) created over a 15 years ago by Jagex Ltd. Like many MMORPGs, one of the major goals in RuneScape is acquiring wealth. One of the most popular methods to do so is called Merchanting. This refers to the act of purchasing an in-game item at a low price and selling that item at a higher price to generate profit. In RuneScape's early history, people merchanted by trading each other directly. That changed with the introducion of the Grand Exchange (abbreviated as GE) in 2007. The Grand Exchange is like an in-game stock market for all of RuneScape. The prices of items are updated depending on recent trade prices and volume. The lower the volume, the less often prices are updated. By predicting the rise and fall of item prices, players can quickly acquire in-game wealth. In this project, I will focus on short and long term price prediction of RuneScape item prices.

### Related Work
#### Several other RuneScape players have had similar ideas, but no finished research has been presented on the current version of the game (One paper on Old School RuneScape Grand Exchange, an older version of the game with a completely separate stock market).

### Dataset: The item_graphs contains 38 CSV files, each corresponding to a different category of in-game item. TODO: Add visualizations of data
Data visualization: https://machinelearningmastery.com/time-series-data-visualization-with-python/

### Methods: Complicated to exactly predict the price. Simplified problem statement. Predict whether prices will increase in the next n days, using prices from the past mdays. Models: Logistic Regression, Bayesian Network, Simple Neural Network, SVM with rbf kernel. Train model(s) for every item on Grand Exchange. Train model(s) on each category of data. Compare. TODO: Everything here

### Conclusions: TODO




## How to Use:

### scrape_graph_info.py
#### Stores item price from the last 180 Days in csv files labeled by category using the Grand Exchange Database API. WARNING: The Grand Exchange has many items, may take 10+ hours to scrape fully

### scrape_items.py
#### Scrapes item names & item ids to a csv file using the Grand Exchange Database API. WARNING: The Grand Exchange has many items, may take multiple hours to scrape all data 

### Steps:

#### Scrape item names and ids using scrape_items.py.
#### Scrape item price for the last 180 Days using scrape_graph_info.py
#### Use machine_learning.py to analyze data (TODO)