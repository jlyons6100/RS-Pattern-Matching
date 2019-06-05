# RS-Pattern-Matching

## Using Machine Learning to Make Predictions on the Runescape Stock Market

### Introduction: 

#### RuneScape is an online fantasy MMORPG (Massively Multiplayer Online Role Playing Game) created over a 15 years ago by Jagex Ltd. Like many MMORPGs, one of the major goals in RuneScape is acquiring wealth. One of the most popular methods to do so is called Merchanting. This refers to the act of purchasing an in-game item at a low price and selling that item at a higher price to generate profit. In RuneScape's early history, people merchanted by trading each other directly. That changed with the introducion of the Grand Exchange (abbreviated as GE) in 2007. The Grand Exchange is like an in-game stock market for all of RuneScape. The prices of items are updated depending on recent trade prices and volume. The lower the volume, the less often prices are updated. By predicting the rise and fall of item prices, players can quickly acquire in-game wealth. In this project, I will focus on short and long term price prediction of RuneScape item prices.

### Related Work:

#### Several other RuneScape players have had similar ideas, but no finished research has been presented on the current version of the game (One paper on Old School RuneScape Grand Exchange, an older version of the game with a completely separate stock market).

### Dataset:

#### The item_graphs contains 38 CSV files, each corresponding to a different category of in-game item. Added graphs of daily item price to see trends visually. Unsuitable graphs: Too flat, price doesn't flucuate much in the short term TODO: Go through each graph and determine which items are even suitable for machine learning. (Clean data)

### Methods: 

#### Complicated to exactly predict the price. Simplified problem statement. Predict whether prices will increase in the next n days, using prices from the past m days. Models: Logistic Regression, Bayesian Network, Simple Neural Network, SVM with rbf kernel. Train model(s) for every item on Grand Exchange. Train model(s) on each category of data. Compare. TODO: Everything here

### Conclusions: 

#### TODO

### Summary of work and Issues:

#### 1. Used python to scrape RuneScape Grand Exchange using Grand Exchange Database API. First, I scraped full list of all item names and item ids. Then I used each item id to scrape previous 180 days worth of price information.
#### Issue 1: Intermittent loss of Internet connection. Solved by wrapping urllib request in a try block nested within a while loop. Continually sends request unless successful.
#### Issue 2: Did not know number limit of queries per second. Too many queries too quickly was causing error. Solved by delaying 5 seconds between query.

#### 2. Created line plots using pyplot and saved as png images.
#### Issue 3: Low Resolution Images. Solved by setting dpi 
#### Issue 4: Rarely a pyplot returns an error when I try to save it as a figure. Solved by wrapping save in a try catch block. Seems that no price change causes this error. Since those don't make for very interesting graphs, it's no loss not to plot them.

### 3. Cleaned data. Completely flat line plots aren't useful. Price doesn't change enough to profit. Also eliminated plots where the price stayed the same for multiple weeks at a time. 

## How to Use:

### scrape_graph_info.py
#### Stores item price from the last 180 Days in csv files labeled by category using the Grand Exchange Database API. WARNING: The Grand Exchange has many items, may take 10+ hours to scrape fully

### scrape_items.py
#### Scrapes item names & item ids to a csv file using the Grand Exchange Database API. WARNING: The Grand Exchange has many items, may take multiple hours to scrape all data 

### Steps:

#### 1. Run scrape_items.py (Scrapes full list of RuneScape item names and ids).
#### 2. Run scrape_graph_info.py(Scrape item price for the last 180 Days) 
#### 3. Use machine_learning.py to analyze data (TODO)
#### Warning: Total Categories may change in the future, so change the number of categories in scrape_items.py and scrape_graph_info.py if it does.