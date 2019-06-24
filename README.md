# RS-Pattern-Matching
Using Machine Learning to Make Predictions on the Runescape Stock Market

### Introduction: 
RuneScape is an online fantasy MMORPG (Massively Multiplayer Online Role Playing Game) created over a 15 years ago by Jagex Ltd. Like many MMORPGs, one of the major goals in RuneScape is acquiring wealth. One of the most popular methods to do so is called Merchanting. This refers to the act of purchasing an in-game item at a low price and selling that item at a higher price to generate profit. In RuneScape's early history, people merchanted by trading each other directly. That changed with the introducion of the Grand Exchange (abbreviated as GE) in 2007. The Grand Exchange is like an in-game stock market for all of RuneScape. The prices of items are updated depending on recent trade prices and volume. The lower the volume, the less often prices are updated. By predicting the rise and fall of item prices, players can quickly acquire in-game wealth. In this project, I will focus on short and long term price prediction of RuneScape item prices.

### Related Work:
Several other RuneScape players have had similar ideas. The initial idea was sparked by a comment by a Jagex employee on a message board years ago stating that he had implemented a basic ML algorithm to predict item price changes and had made so much money in such a short time that the game's creators investigated him, thinking that he was cheating. 

### Dataset:
The item_graphs folder contains 38 CSV files, each corresponding to a different category of in-game item. The previous 180 days of price data for 5800 or so items is stored in csv files within. I created graphs of daily item prices to the data_visaulization folder to see trends visually before working on the machine learning models. Unsuitable items: Too flat - price doesn't fluctuate much, if at all in the short term. Only increasing/decreasing - There will only be one class. Whichever models I use won't have any way to determine what the opposite class looks like.

### Methods: 
It would be complicated to exactly predict the price. Instead I simplified my problem statement. I will predict whether prices will increase in the next n days, using prices from the past m days. For an individual item, start at 180 days ago. Train using day -180 to day -180+m. Predict on -180+m+n. Repeat. Models: Logistic Regression, Bayesian Network, Simple Neural Network, SVM with rbf kernel. As a beginning to ML, I'm not sure that a model trained on all of the data in the Grand Exchange would be more accurate than if I tailored my models to the individual items. I will test out the theory that the ML models are more accurate for single items through the following methods. I will train models for every item on Grand Exchange. Then I'll train model(s) on each category of data (Must normalize data). Finally I'll train models using normalized data from every item at once. No significant difference in % chance of a price increase despite these three approaches, possibly indicating that there aren't many categorical trends or trends for the entire market in the short term. Compare. TODO: Everything here

### Results: 
![Table 1](https://github.com/jlyons6100/RS-Pattern-Matching/blob/master/Tables/Table%201.png)
![Table 2](https://github.com/jlyons6100/RS-Pattern-Matching/blob/master/Tables/Table%202.png)
![Table 3](https://github.com/jlyons6100/RS-Pattern-Matching/blob/master/Tables/Table%203.png)

Surprisingly, I was completely wrong. The models trained on the entire grand exchange before slightly better than the models trained on categories and individual items. This difference increased with predictions further in the future.

### Summary of work and Issues:

1. Used python to scrape RuneScape Grand Exchange using Grand Exchange Database API. First, I scraped full list of all item names and item ids. Then I used each item id to scrape previous 180 days worth of price information.
Issue 1: Intermittent loss of Internet connection. Solved by wrapping urllib request in a try block nested within a while loop. Continually sends request unless successful.
Issue 2: Did not know number limit of queries per second. Too many queries too quickly was causing error. Solved by delaying 5 seconds between query.

2. Created line plots using pyplot and saved as png images.
Issue 3: Low Resolution Images. Solved by setting dpi 
Issue 4: Rarely a pyplot returns an error when I try to save it as a figure. Solved by wrapping save in a try catch block. Seems that no price change causes this error. Since those don't make for very interesting graphs, it's no loss not to plot them.

3. Cleaned data. Completely flat line plots aren't useful. Price doesn't change enough to profit. Also eliminated plots where the price stayed the same for multiple weeks at a time. Additionally, highly irregular graphs can indicate special circumstances such as Price Manipulation (Large groups of people artificially raise price to profit) and obsolete items (With the introduction of new better items, some older items are no longer traded) 

4. Created 3 machine_learning_X.py files. Outputs saved to simple text files, model names next to accuracies. TODO: Create table of accuracy values for visualization.
Issue 5: I don't know anything about machine learning. I solved this issue by reading an introduction to machine learning on a programming site and working through "Hello World" type Machine Learning programs.
Issue 6: SVM with an rbf kernel was running infinitely on an input dataset of 936,000 points. I solved this by reading that on "above the 200,000 observation range, it's wise to pick linear learners." Since I have nearly a million observations, I don't think it would be wise for me to use SVM  in this case.

### How to Use:

#### 1. Run scrape_items.py (Scrapes full list of RuneScape item names and ids).
#### 2. Run scrape_graph_info.py(Scrape item price for the last 180 Days) 
#### 3. Use data_vis.py to iterate through item price graphs and create simple line plots of them.
#### 4. Use machine_learning_X.py to analyze the effectiveness of 5-6 ML models for predictions on this data.
#### 5. Use the output of machine_learning_X.py to create tables of (m,n) pairs and model names along with accuracy %'s.
#### Warning: Total Categories may change in the future, so change the number of categories in scrape_items.py and scrape_graph_info.py if it does.

### File Descriptions:
#### Tables - Contains images of accuracy values for models
#### data_nov_18 - Data scraped November 18, 2018
#### data_visualization - Contains image graphs of item values over last 180 days
#### item_graphs - Contains 180 days worth of price data for all 5800 items on the Grand Exchange
#### items_to_ids - Contains item names mapped to item ids on the Grand Exchange
#### model_per_all - Contains accuracy values of models trained on the entire dataset (936,000 data points)
#### model_per_category - Contains accuracy values of models trained on the each category (38 Categories)
#### model_per_item - Contains accuracy values of models trained on each item (5800 items)
#### data_vis.py - Creates images of the average price to see trends visually
#### machine_learning_all.py - Generates accuracy values for models trained on entire dataset
#### machine_learning_cat.py - Generates accuracy values for models trained on each category
#### machine_learning_item.py - Generates accuracy values for models trained on individual items
#### scrape_graph_info.py - Stores item price from the last 180 Days in csv files labeled by category using the Grand Exchange Database API. WARNING: The Grand Exchange has many items, may take 10+ hours to scrape fully

#### scrape_items.py - Scrapes item names & item ids to a csv file using the Grand Exchange Database API. WARNING: The Grand Exchange has many items, may take multiple hours to scrape all data 
