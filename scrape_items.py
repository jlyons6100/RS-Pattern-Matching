import urllib.request
import csv
import json
import os.path
import string
import time

num_categories = 22
item_ids = {}

def handle_file_data():
    for category in range(1, num_categories+1):
        for letter in string.ascii_lowercase:
            for page in range(1, 1000):
                #print("Item data: Category "+str(category)+" Letter " +str(letter) +" page "+str(page))
                pg = urllib.request.urlopen('http://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?category='
                 + str(category)+'&alpha='
                 +letter + '&page='+str(page))
                html = pg.read()
                try:
                    time.sleep(5) # Without pause, Runescape API returns errors, too many requests too fast
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
def main():
    handle_file_data()
main()
