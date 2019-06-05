import urllib.request
import csv
import json
import os.path
import string
import time

# Category names
cat_names = ["Miscellaneous","Ammo", "Arrows", "Bolts", "Construction_Materials"
, "Construction_Projects", "Cooking_Ingredients","Costumes"
,"Crafting_Materials","Familiars","Farming_Produce","Fletching_Materials"
,"Food_and_Drink","Herblore_Materials","Hunting_Equipment","Hunting_Produce"
,"Jewellery","Mage_Armour","Mage_Weapons", "Melee_Armor_Low_Level","Melee_Armor_Mid_Level",
"Melee_Armor_High_Level","Melee_Weapons_Low_Level","Melee_Weapons_Mid_Level","Melee_Weapons_High_Level","Mining_and_Smithing","Potions","Prayer_Armour","Prayer_Materials",
"Range_Armour","Range_Weapons","Runecrafting","Runes_Spells_Teleports","Seeds","Summoning_Scrolls",
"Tools_and_Containers","Woodcutting_Products","Pocket_Items"]

max_pages = 1000

# Stores item name and ID for all items on the Grand Exchange (Runescape Stock Market)
def handle_file_data():
    for category in range(0, len(cat_names)):
        item_ids = {}
        for letter in string.ascii_lowercase:
            for page in range(1, max_pages):
                while True: # While loop to keep trying to scrape even if your Internet goes in and out
                    try:
                        pg = urllib.request.urlopen('http://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?category='
                        + str(category)+'&alpha='
                        +letter + '&page='+str(page))
                        html = pg.read()
                        break
                    except:    
                        pass
                try:
                    time.sleep(5) # Spam API at your own risk
                    parsed_json = json.loads(html)
                    if (len(parsed_json["items"]) == 0):
                        break
                    for item in parsed_json["items"]:
                        print(item['name'])
                        item_ids[item['name']] = item['id']
                except:
                    print("FAILED Item data: Category "+str(category)+" Letter " +str(letter) +" page "+str(page))
                    continue
        with open('items_to_ids/' + cat_names[category]+'.csv', 'w') as csvfile:
            fieldnames = ["name", "id"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for name in item_ids:
                writer.writerow({"name": name,"id": item_ids[name],})
        print("Scraped Category: "+cat_names[category]) 

handle_file_data()

