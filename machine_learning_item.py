import urllib.request
import csv
import json
import os.path
import string
import time
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from sklearn import preprocessing
#from pandas.plotting import scatter_matrix
#import matplotlib.pyplot as plt
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


cat_names = ["Miscellaneous","Ammo", "Arrows", "Bolts", "Construction_Materials"
, "Construction_Projects", "Cooking_Ingredients","Costumes"
,"Crafting_Materials","Familiars","Farming_Produce","Fletching_Materials"
,"Food_and_Drink","Herblore_Materials","Hunting_Equipment","Hunting_Produce"
,"Jewellery","Mage_Armour","Mage_Weapons", "Melee_Armor_Low_Level","Melee_Armor_Mid_Level",
"Melee_Armor_High_Level","Melee_Weapons_Low_Level","Melee_Weapons_Mid_Level","Melee_Weapons_High_Level","Mining_and_Smithing","Potions","Prayer_Armour","Prayer_Materials",
"Range_Armour","Range_Weapons","Runecrafting","Runes_Spells_Teleports","Seeds","Summoning_Scrolls",
"Tools_and_Containers","Woodcutting_Products","Pocket_Items"]

models = []
models.append(('LogisticRegression', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LinearDiscriminantAnalysis', LinearDiscriminantAnalysis()))
models.append(('KNeighborsClassifier', KNeighborsClassifier()))
models.append(('DecisionTreeClassifier', DecisionTreeClassifier()))
models.append(('GaussianNB', GaussianNB()))
models.append(('SVM w/ rbf kernel', SVC(gamma='auto', kernel='rbf')))

m = 7 # Prices from the past m days
n = 7 # Predict if price increases over the next n days. #Combined needs to factor of 180 
n_splits = 10 # Number of k-fold splits, decrease this number if it doesn't work due to large m + n size

def get_data_from_row(row):
    global models
    arr = list(row)
    minn = min(arr)
    for x in range(len(arr)):
        arr[x] = arr[x] - minn
    maxx = max(arr)
    for x in range(len(arr)):
        if arr[x] != 0:
            arr[x] = maxx / arr[x] 
    global m, n, n_splits
    X = []
    Y = []
    true_set = set()
    for x in range(0, len(arr)-m-n, m+n+1):
        past_m = list(arr[x:x+m])
        X.append(past_m)
        next_n = True if arr[x+m] < arr[x+m+n] else False
        Y.append(next_n)
        true_set.add(next_n)
    if len(true_set) == 1: 
        return [], []
    return X, Y
def test_models(X, Y, values):
    global n_splits, models
    try:
        validation_size = 0.00
        seed = 7
        scoring = "accuracy"
        results = []
        names = []
        for name, model in models:
            kfold = model_selection.KFold(n_splits=n_splits, random_state=seed)
            cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            if name not in values:
                values[name] = [cv_results.mean()]
            else:
                values[name].append(cv_results.mean())
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    except:
        pass
def test_models_on_cat(model_averages, headers, cat):
    #print("Category: "+ cat)
    df = pd.read_csv("item_graphs/"+cat+".csv", names=headers, index_col = 0)
    X = []
    Y = []
    # Calculating ML for each item in a category
    for index, row in df.iterrows():
        new_X, new_Y = get_data_from_row(row)
        if len(new_X) != 0:
            test_models(new_X, new_Y, model_averages)

def machine_learning():
    headers = []
    headers.append("Name")
    global m,n
    for x in  range(-179, 1):
        headers.append(x)
    sum_of_avr = []
    model_averages = {}
    #print("Model Averages for EACH Category")
    
    for cat in cat_names:
        print("Model Averages for "+cat+" Category: (" +str(m) + ","+str(n)+")")
        test_models_on_cat(model_averages, headers, cat)
    #print(sum(sum_of_avr)/len(sum_of_avr))
    print("Overall Averages: (" +str(m) + ","+str(n)+")")
    for model_name in model_averages:
        print(model_name)
        print(sum(model_averages[model_name])/len(model_averages[model_name]))

machine_learning()
# python3 -W ignore machine_learning.py  to suppress warnings about collinear variables   
