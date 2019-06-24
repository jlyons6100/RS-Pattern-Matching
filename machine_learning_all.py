import urllib.request
import csv
import json
import os.path
import string
import time
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Runescape item category names
cat_names = ["Miscellaneous","Ammo", "Arrows", "Bolts", "Construction_Materials"
, "Construction_Projects", "Cooking_Ingredients","Costumes"
,"Crafting_Materials","Familiars","Farming_Produce","Fletching_Materials"
,"Food_and_Drink","Herblore_Materials","Hunting_Equipment","Hunting_Produce"
,"Jewellery","Mage_Armour","Mage_Weapons", "Melee_Armor_Low_Level","Melee_Armor_Mid_Level",
"Melee_Armor_High_Level","Melee_Weapons_Low_Level","Melee_Weapons_Mid_Level","Melee_Weapons_High_Level","Mining_and_Smithing","Potions","Prayer_Armour","Prayer_Materials",
"Range_Armour","Range_Weapons","Runecrafting","Runes_Spells_Teleports","Seeds","Summoning_Scrolls",
"Tools_and_Containers","Woodcutting_Products","Pocket_Items"]

def get_data_from_row(row, m, n):
    arr = list(row)
    # NORMALIZING DATA FROM ARR
    minn = min(arr)
    for x in range(len(arr)):
        arr[x] = arr[x] - minn
    maxx = max(arr)
    for x in range(len(arr)):
        if arr[x] != 0:
            arr[x] = maxx / arr[x]
    # NORMALIZING DATA FROM ARR
    row_X = []
    row_Y = []
    true_set = set()
    # Predict if price increases over the next n days based on the previous m
    for x in range(0, len(arr)-m-n, m+n+1):
        past_m = list(arr[x:x+m])
        row_X.append(past_m)
        next_n = True if arr[x+m] < arr[x+m+n] else False # True if price increased over next n days
        row_Y.append(next_n)
        true_set.add(next_n)
    # Making sure all data points aren't in the same class, not useful for ML
    if len(true_set) == 1: 
        return [], []
    return row_X, row_Y
def test_models(X, Y):
    models = []
    models.append(('LogisticRegression', LogisticRegression(solver='liblinear', multi_class='ovr')))
    models.append(('LinearDiscriminantAnalysis', LinearDiscriminantAnalysis()))
    models.append(('KNeighborsClassifier', KNeighborsClassifier()))
    models.append(('DecisionTreeClassifier', DecisionTreeClassifier()))
    models.append(('GaussianNB', GaussianNB()))
    # SVM problems with more than 200,000 data points
    n_splits = 10 # Number of k-fold splits, decrease this number if it doesn't work due to large m + n size
    seed = 7
    scoring = "accuracy"
    results = []
    names = []   
    for name, model in models:
        kfold = model_selection.KFold(n_splits=n_splits, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
def get_cat_data(headers, cat, m, n):
    df = pd.read_csv("item_graphs/"+cat+".csv", names=headers, index_col = 0)
    cat_X = []
    cat_Y = []
    for index, row in df.iterrows():
        row_X, row_Y = get_data_from_row(row, m, n)
        cat_X.extend(row_X)
        cat_Y.extend(row_Y)
    return cat_X, cat_Y
# machine_learning(m, n): Tests models for ML, price increase in next n days based on previous m days of data
def machine_learning(m, n):
    headers = ["Name"] + [x for x in range(-179, 1)]
    all_X = []
    all_Y = []
    for cat in cat_names:
        print("Data for "+cat+" Category: (" +str(m) + ","+str(n)+")")
        cat_X, cat_Y = get_cat_data(headers, cat, m, n)
        all_X.extend(cat_X)
        all_Y.extend(cat_Y)
    print("Testing Models:")
    test_models(all_X, all_Y)

machine_learning(4,2) 
# Run with python3 -W ignore machine_learning.py  to suppress warnings about collinear variables   
