import os
import pandas 
from matplotlib import pyplot as plt

# Category names
cat_names = ["Miscellaneous","Ammo", "Arrows", "Bolts", "Construction_Materials"
, "Construction_Projects", "Cooking_Ingredients","Costumes"
,"Crafting_Materials","Familiars","Farming_Produce","Fletching_Materials"
,"Food_and_Drink","Herblore_Materials","Hunting_Equipment","Hunting_Produce"
,"Jewellery","Mage_Armour","Mage_Weapons", "Melee_Armor_Low_Level","Melee_Armor_Mid_Level",
"Melee_Armor_High_Level","Melee_Weapons_Low_Level","Melee_Weapons_Mid_Level","Melee_Weapons_High_Level","Mining_and_Smithing","Potions","Prayer_Armour","Prayer_Materials",
"Range_Armour","Range_Weapons","Runecrafting","Runes_Spells_Teleports","Seeds","Summoning_Scrolls",
"Tools_and_Containers","Woodcutting_Products","Pocket_Items"]

header = []
for x in  range(-179, 1):
    header.append(x)


# Make graph of one item
def make_plot(cat):
    series = pandas.read_csv("item_graphs/"+cat+".csv", names = header,index_col = 0)
    #series = pandas.read_csv(cat+".csv", names = header, index_col = 0)
    series = series.T
    #print(series)
    #return

    for column in series.columns:
        ax = series.plot(y=column, title = column+" Price")
        ax.set_xlabel("Days since June 4, 2019")
        ax.set_ylabel("RuneScape Gold")
        ax.get_legend().remove()
        try:
            plt.savefig("data_visualization/"+cat+"/"+column+ '.png', dpi=400)
            print("Created graph for: "+column)
            plt.close('all')
        except:
            print("Can't save: "+column)
        

   
for cat in cat_names:
    make_plot(cat)


def make_directories():
    for cat in cat_names:
        os.makedirs("data_visualization/"+cat)
#make_directories()
