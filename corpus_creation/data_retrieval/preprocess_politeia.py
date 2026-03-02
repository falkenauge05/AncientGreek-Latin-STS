from lxml import etree
import re
import random
import numpy as np
import csv

# Load XML file
tree = etree.parse("eng_grc_data/politeia_grc.xml")
root_grc = tree.getroot()
tree = etree.parse("eng_grc_data/politeia_eng.xml")
root_lat = tree.getroot()

# TEI namespace (REQUIRED)
ns = {"tei": "http://www.tei-c.org/ns/1.0"}
n1=1#11, 447
first_loop=True
#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@n='$1']/tei:div[@n='$2']/tei:div[@n='$3'])

# Run XPath
# Process results
results_grc = [' ']
results_lat = [' ']
res_list=[]
while n1<622: #results_grc!=[] and results_lat!=[]:
    xpath = f"/tei:TEI/tei:text/tei:body/tei:div//tei:div[@n='{str(n1)}' and @subtype='section']"
    results_grc = root_grc.xpath(xpath, namespaces=ns)
    results_lat = root_lat.xpath(xpath, namespaces=ns)
    while first_loop and (results_grc == [] and results_lat == []):
        n1+=1
        xpath = f"/tei:TEI/tei:text/tei:body/tei:div//tei:div[@n='{str(n1)}' and @subtype='section']"
        results_grc = root_grc.xpath(xpath, namespaces=ns)
        results_lat = root_lat.xpath(xpath, namespaces=ns)
    first_loop=False

    if results_grc != [] and results_lat != []:
        res_grc = results_grc[0].xpath(".//text()[not(ancestor::tei:note or ancestor::tei:bibl or ancestor::tei:cit)]", namespaces=ns)
        res_grc = " ".join(res_grc).strip()
        res_grc = re.sub(r"\s+", " ", res_grc)
        res_lat = results_lat[0].xpath(".//text()[not(ancestor::tei:note or ancestor::tei:bibl or ancestor::tei:cit)]", namespaces=ns)
        res_lat = " ".join(res_lat).strip()
        res_lat = re.sub(r"\s+", " ", res_lat)
        res_list.append((res_grc, res_lat))
    else:
        if (results_grc == [] and results_lat != []):
            res_lat = re.sub(r"\s+", " ", " ".join(results_lat[0].itertext()).strip())
            res_list[len(res_list) - 1] = (res_list[len(res_list) - 1][0],
                                           res_list[len(res_list) - 1][1] + " " + res_lat)
            # print(res_list[len(res_list)-1])
        if results_grc != [] and results_lat == []:
            print(re.sub(r"\s+", " ", " ".join(results_grc[0].itertext()).strip()))
    n1+=1

res_list_final=[]
cur_res_grc=""
cur_res_lat=""
for res_grc, res_lat in res_list:
    if re.search(r'[A-Za-z]', res_grc):
        print(res_grc)
    if "Plat." in res_lat:
        print(res_lat)
    if "Plat." in res_grc:
        print(res_grc)
    if len(res_grc.split())>100:
        split_grc = res_grc.split("ΣΩ.")
        split_lat = res_lat.split("Soc.")
        #split_grc = [elem for sgl_list in [spl.split("ΚΡ.") for spl in split_grc] for elem in sgl_list]
        #split_lat = [elem for sgl_list in [spl.split("Crit.") for spl in split_lat] for elem in sgl_list]
        if len(split_grc)!=len(split_lat):
            print("AAHHH!")
            print(res_grc)
            print(res_lat)
            print(len(split_grc))
            print(len(split_lat))
        res_list_final.extend([(split_grc[i].strip(), split_lat[i].strip()) for i in range(len(split_grc)) if split_grc[i]!=""])
    else:
        res_list_final.append((res_grc, res_lat))

print(np.mean([len(r[0].split()) for r in res_list_final]))
#random.seed(42)
#random.shuffle(res_list)
with open("grc_eng_training.csv", 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(res_list_final)