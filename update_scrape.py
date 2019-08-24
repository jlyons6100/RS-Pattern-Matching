import urllib.request
import csv
import json
import os.path
import string
import time
from copy import deepcopy
# 22 total categories as of November 18, 2018
# 38 total categories as of June 4, 2019
cat_names = ["Miscellaneous","Ammo", "Arrows", "Bolts", "Construction_Materials"
, "Construction_Projects", "Cooking_Ingredients","Costumes"
,"Crafting_Materials","Familiars","Farming_Produce","Fletching_Materials"
,"Food_and_Drink","Herblore_Materials","Hunting_Equipment","Hunting_Produce"
,"Jewellery","Mage_Armour","Mage_Weapons", "Melee_Armor_Low_Level","Melee_Armor_Mid_Level",
"Melee_Armor_High_Level","Melee_Weapons_Low_Level","Melee_Weapons_Mid_Level","Melee_Weapons_High_Level","Mining_and_Smithing","Potions","Prayer_Armour","Prayer_Materials",
"Range_Armour","Range_Weapons","Runecrafting","Runes_Spells_Teleports","Seeds","Summoning_Scrolls",
"Tools_and_Containers","Woodcutting_Products","Pocket_Items"]

item_cat_data = []
 
# Reads in ids and names of all items in Grand Exchange from csv file
def read_ids_from_csv():
    for i, cat in enumerate(cat_names):
        item_ids = {}
        with open('items_to_ids/'+cat+'.csv') as csvfile:
        # with open(cat+'.csv') as csvfile:
            fieldnames = ['name', 'id']
            reader = csv.DictReader(csvfile, fieldnames = fieldnames)
            for row in reader:
                item_ids[row['name']] = row['id']
        item_cat_data.append(item_ids)
header = None
def get_old_data(cat):
    old_data = {}
    with open('database/'+cat+'.csv', 'r') as f:
        # global header
        d_reader = csv.DictReader(f)
        # if header == None:
            # header = d_reader.fieldnames
        
        for line in d_reader:
            new_line = []
            for value in (line.items()):
                if value[0] != 'name':
                    new_line.append(value)
            old_data[line['name']] = new_line
    return old_data
    
# Requests graph data for all items in Grand Exchange
def scrape_graphs():
    for ind in  range(len(item_cat_data)):
        old_data = get_old_data(cat_names[ind])
        for i, item_name in enumerate(item_cat_data[ind]):
            if item_name not in old_data:
                continue
            item_id = item_cat_data[ind][item_name]
            times_tried = 0
            while True:
                try:
                    pg = urllib.request.urlopen('http://services.runescape.com/m=itemdb_rs/api/graph/'+str(item_id)+'.json') 
                    html = pg.read()
                    time.sleep(5) # Without pause, Runescape API returns errors, too many requests too fast
                    parsed_json = json.loads(html)
                    new_arr = []
                    for ms in parsed_json["daily"]:
                        days = str(float(ms) / (1000 * 60 * 60 * 24))
                        last_tup = old_data[item_name][len(old_data[item_name]) - 1]

                        if  float(days) > float(last_tup[0]):
                            old_data[item_name].append((days,parsed_json["daily"][ms]))
                        else:
                            try:
                                prev_ind = old_data[item_name].index((days, '-1'))
                                old_data[item_name][prev_ind] = (days,parsed_json["daily"][ms])
                            except:
                                pass
                    print(item_name)
                    break
                except:
                    
                    if times_tried < 30:
                        print("Retrying request: " + str(item_name))
                    else:
                        print("Failed request: " + str(item_name))
                        break
                    times_tried += 1
        with open('database/'+cat_names[ind]+'.csv', 'w') as csvfile:
            item_name = ""
            for key in old_data:
                item_name = key
                break
            fieldnames = ['name'] + [tup[0] for tup in old_data[item_name]]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # print(fieldnames)
            # print(sorted(old_data[item_name]))
            for item_name in old_data:
                # if not item_name in old_data:
                    # continue
                row_dict = {'name':item_name}
                for tup in old_data[item_name]:
                    if tup[0] in fieldnames:
                        row_dict[tup[0]] = tup[1]
                for day in fieldnames:
                    if day not in row_dict:
                        row_dict[day] = '-1'
                writer.writerow(row_dict)
        print("Updated Graphs for Category: "+cat_names[ind])
        # exit(0)
read_ids_from_csv()
scrape_graphs()

