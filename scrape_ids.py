import urllib.request
import csv
import json
import os.path
import string
import time
#string.ascii_lowercase = all letters in a string

num_categories = 22
item_ids = {}
#ITEM_DATA_CSV = 'item_data.csv'
# Checking to see if I need to scrap the data again / need to create the csv file
def handle_file_data():
    for category in range(1, num_categories+1):
        for letter in string.ascii_lowercase:#string.ascii_lowercase
            for page in range(1, 1000): # No way there's actually 1000 pages
                print("Item data: Category "+str(category)+" Letter " +str(letter) +" page "+str(page))
                pg = urllib.request.urlopen('http://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?category='
                 + str(category)+'&alpha='
                 +letter + '&page='+str(page))
                html = pg.read()

                try:
                    time.sleep(5)
                    parsed_json = json.loads(html)
                    #print(len(parsed_json["items"]))
                    if (len(parsed_json["items"]) == 0):
                        break
                    for item in parsed_json["items"]:
                        item_ids[item['name']] = item['id']
                except:
                    print("FAILED Item data: Category "+str(category)+" Letter " +str(letter) +" page "+str(page))
                    continue

    with open('item_ids.csv', 'w') as csvfile:
        fieldnames = ["name", "id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for name in item_ids:
            writer.writerow({"name": name,"id": item_ids[name],})
    print("Scraped Grand Exchange Item ID and Name to item_ids.csv, exiting")
                    
    #print("hello")
    #print(parsed_json)
    # if(os.path.isfile(ITEM_DATA_CSV)):
        # print("File " + ITEM_DATA_CSV+ " Already Existed:")
    #Check runedate here to see if I need to reload
    # with open(ITEM_DATA_CSV, 'a+') as f:
    #     csvwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     print("No " + ITEM_DATA_CSV + " file found, creating new.")
    #     csvwriter.writerow(['lastConfigUpdateRuneday', parsed_json["lastConfigUpdateRuneday"]])
def main():
    handle_file_data()
    #check_rune_date()

main()
