from lxml import etree
import re
import random
import csv

# Load XML file
tree = etree.parse("thukydides_grc.xml")
root_grc = tree.getroot()
tree = etree.parse("thukydides_lat.xml")
root_lat = tree.getroot()

# TEI namespace (REQUIRED)
ns = {"tei": "http://www.tei-c.org/ns/1.0"}

# Your dynamic values
n1 = 1   # replaces $1
n2 = 1   # replaces $2
n3 = 1

#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@n='$1']/tei:div[@n='$2']/tei:div[@n='$3'])

# Run XPath
# Process results
results_grc = [' ']
results_lat = [' ']
empty = False
double_empty = False
loop_chapter=True
loop_book=True
res_list=[]
while loop_book:
    n2=1
    loop_chapter=True
    while loop_chapter:
        n3=1
        results_grc = [' ']
        results_lat = [' ']
        while results_grc!=[] and results_lat!=[]:
            xpath = f"/tei:TEI/tei:text/tei:body/tei:div/tei:div[@n='{str(n1)}']/tei:div[@n='{str(n2)}']/tei:div[@n='{str(n3)}']"
            results_grc = root_grc.xpath(xpath, namespaces=ns)
            results_lat = root_lat.xpath(xpath, namespaces=ns)

            if double_empty and results_grc==[] and results_lat==[]:
                loop_book=False
            if results_grc==[] and results_lat==[] and empty:
                loop_chapter=False
                double_empty = True
            if results_grc != [] and results_lat != []:
                res_grc = " ".join(results_grc[0].itertext()).strip()
                res_grc = re.sub(r"\s+", " ", res_grc)
                res_lat = " ".join(results_lat[0].itertext()).strip()
                res_lat = re.sub(r"\s+", " ", res_lat)
                res_list.append((res_grc, res_lat))
                empty = False
                double_empty = False
            else:
                if (results_grc == [] and results_lat != []):
                    res_lat=re.sub(r"\s+", " ", " ".join(results_lat[0].itertext()).strip())
                    res_list[len(res_list)-1]=(res_list[len(res_list)-1][0], res_list[len(res_list)-1][1]+" "+res_lat)
                    #print(res_list[len(res_list)-1])
                if results_grc != [] and results_lat == []:
                    print(re.sub(r"\s+", " ", " ".join(results_grc[0].itertext()).strip()))
                empty=True
            n3+=1
        n2+=1
    n1+=1

res_list_final=[]
for res_grc, res_lat in res_list:
    res_lat = res_lat.replace("j", "i")
    res_lat = res_lat.replace("æ", "ae")
    res_lat = res_lat.replace("Æ", "Ae")
    res_lat = res_lat.replace("œ", "oe")
    res_list_final.append((res_grc, res_lat))
    if re.search(r'[A-Za-z]', res_grc):
        print(res_grc)
random.seed(42)
random.shuffle(res_list_final)
with open("training.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(res_list_final)