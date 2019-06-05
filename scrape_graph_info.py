import urllib.request
import csv
import json
import os.path
import string
import time

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
    for cat in cat_names:
        item_ids = {}
        with open('items_to_ids/'+cat+'.csv') as csvfile:
            fieldnames = ['name', 'id']
            reader = csv.DictReader(csvfile, fieldnames = fieldnames)
            for row in reader:
                item_ids[row['name']] = row['id']
        item_cat_data.append(item_ids)

# Requests graph data for all items in Grand Exchange
def scrape_graphs():
    for ind in  range(len(item_cat_data)):
        #if ind != 3:
            #continue
        item_graphs = {}
        for item_name in item_cat_data[ind]:
            item_id = item_cat_data[ind][item_name]
            while True:
                try:
                    pg = urllib.request.urlopen('http://services.runescape.com/m=itemdb_rs/api/graph/'+str(item_id)+'.json') 
                    html = pg.read()
                    break
                except:    
                    pass
            try:
                time.sleep(5) # Without pause, Runescape API returns errors, too many requests too fast
                parsed_json = json.loads(html)
                new_arr = []
                for day in parsed_json["daily"]:
                    new_arr.append(parsed_json["daily"][day])  # Array goes from 180 days ago until now
                item_graphs[item_name] = new_arr
                print(item_name)
            except:
                print("Failed request")
                continue
        with open('item_graphs/'+cat_names[ind]+'.csv', 'w') as csvfile:
            fieldnames = ["name"] + list(range(1, 180+1))
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for item_name in item_graphs:
                row_dict = {"name":item_name}
                for x in range(1, 180+1):
                    row_dict[x] = item_graphs[item_name][x-1]
                # for x in item_graphs[item_name][0]:
                #     row_dict[x] = item_graphs[name][0][x]
                writer.writerow(row_dict)
        print("Created Graphs for Category: "+cat_names[ind])

read_ids_from_csv()
scrape_graphs()

