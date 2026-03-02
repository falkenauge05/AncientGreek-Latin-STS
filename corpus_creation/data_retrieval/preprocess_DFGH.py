import csv
from lxml import etree
import pathlib
import random
import re

directories = [pathlib.Path("../../data/Training_Data_DFGH/volume_1-master/data/xml"),
               pathlib.Path("../../data/Training_Data_DFGH/volume_2-master/data/xml"),
               pathlib.Path("../../data/Training_Data_DFGH/volume_3-master/data/xml"),
               pathlib.Path("../../data/Training_Data_DFGH/volume_4-master/data/xml"),
               pathlib.Path("../../data/Training_Data_DFGH/volume_5_1-master/data/xml"),
               pathlib.Path("../../data/Training_Data_DFGH/volume_5_2-master/data/xml"),]
files=list([list(directory.rglob("*.xml")) for directory in directories])
files=[el for lst in files for el in lst]
res_list=[]
for file in files:
    tree=etree.parse(file)
    for fragment in tree.findall(".//fragment"):
        text=fragment.find("./text").text
        translation=fragment.find("./translation").text
        if not text is None and not translation is None and 3<len(text.split(" "))<500 and 3<len(translation.split(" "))<500:
            res_list.append((text, translation))
res_list_final=[]
for res_grc, res_lat in res_list:
    res_lat = res_lat.replace("j", "i")
    res_lat = res_lat.replace("æ", "ae")
    res_lat = res_lat.replace("Æ", "Ae")
    res_lat = res_lat.replace("œ", "oe")
    res_lat = re.sub(r"\s+", " ", res_lat).strip()
    res_grc = re.sub(r"\s+", " ", res_grc).strip()
    res_list_final.append((res_grc, res_lat))
random.seed(42)
random.shuffle(res_list_final)
with open("training.csv", 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(res_list_final)