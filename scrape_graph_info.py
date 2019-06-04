import urllib.request
import csv
import json
import os.path
import string
import time

# 22 total categories as of November 18, 2018
# 37 total categories as of June 4, 2019
num_categories = 22
item_ids = {}
item_graphs = {}
 
# Reads in ids and names of all items in Grand Exchange from csv file
def read_ids_from_csv():
    with open('item_ids.csv') as csvfile:
        fieldnames = ['name', 'id']
        reader = csv.DictReader(csvfile, fieldnames = fieldnames)
        for row in reader:
            item_ids[row['name']] = row['id']

# Requests graph data for all items in Grand Exchange
def scrape_graphs():
    for item_name in item_ids:
        print(str(item_ids[item_name]))
        pg = urllib.request.urlopen('http://services.runescape.com/m=itemdb_rs/api/graph/'+str(item_ids[item_name])+'.json') # should add try catch here
        html = pg.read()
        try:
            time.sleep(5) # Without pause, Runescape API returns errors, too many requests too fast
            parsed_json = json.loads(html)
            
            # Sorted for order
            day_count = 1 # 180 days ago
            new_daily = {} 
            # Replace "daily" with "average" to get average instead
            for x in parsed_json["daily"]: # This shouldn't be sorted. 
                new_daily[day_count] = parsed_json["daily"][x]
                day_count += 1
            
            
            item_graphs[item_name] = [new_daily]
        except:
            print("Failed request")
            continue
        break
        # break for one data point instead of all

# Saves graph data to csv file. First entry is 180 days ago, last entry is from today        
def save_to_csv():
    with open('item_graphs.csv', 'w') as csvfile:
        fieldnames = ["name"] + list(range(1, 180+1))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for name in item_graphs:
            row_dict = {"name":name}
            for x in item_graphs[name][0]:
                row_dict[x] = item_graphs[name][0][x]
            writer.writerow(row_dict)
       
def main():
    read_ids_from_csv()
    scrape_graphs()
    save_to_csv()
main()
