import urllib.request
import csv
import json
import os.path

ITEM_DATA_CSV = 'item_data.csv'

# Checking to see if I need to scrap the data again / need to create the csv file
def handle_file_data():
    pg = urllib.request.urlopen('https://secure.runescape.com/m=itemdb_rs/api/info.json')
    html = pg.read()
    parsed_json = json.loads(html)
    
    if(os.path.isfile(ITEM_DATA_CSV)):
        print("File " + ITEM_DATA_CSV+ " Already Existed:")
    #Check runedate here to see if I need to reload
    with open(ITEM_DATA_CSV, 'a+') as f:
        csvwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("No " + ITEM_DATA_CSV + " file found, creating new.")
        csvwriter.writerow(['lastConfigUpdateRuneday', parsed_json["lastConfigUpdateRuneday"]])
def main():
    create_csv_file
    check_rune_date()

check_rune_date()
