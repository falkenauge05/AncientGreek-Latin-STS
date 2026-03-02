from lxml import etree
import re
import random
import numpy as np
import csv

# Load XML file
tree = etree.parse("eng_grc_data/ilias_grc.xml")
root_grc = tree.getroot()

# TEI namespace (REQUIRED)
ns = {"tei": "http://www.tei-c.org/ns/1.0"}
n1=1#11, 447
n2=1
first_loop=True
#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@n='$1']/tei:div[@n='$2']/tei:div[@n='$3'])

# Run XPath
# Find out greek result (Iliad in lines)
results_grc = [' ']
grc_res={}
empty=False
while True:
    xpath = f"/tei:TEI/tei:text/tei:body/tei:div/tei:div[@n='{str(n1)}']//tei:l[@n='{str(n2)}']"
    results_grc = root_grc.xpath(xpath, namespaces=ns)

    if results_grc:
        res_grc = results_grc[0].xpath(".//text()[not(ancestor::tei:note or ancestor::tei:bibl or ancestor::tei:cit)]", namespaces=ns)
        res_grc = " ".join(res_grc).strip()
        res_grc = re.sub(r"\s+", " ", res_grc)
        if n1 in grc_res:
            grc_res[n1].append(res_grc)
        else:
            grc_res[n1]=[res_grc]
        empty=False
    else:
        if empty:
            break
        n1+=1
        n2=1
        empty=True
    n2+=1

tree = etree.parse("eng_grc_data/ilias_eng.xml")
root = tree.getroot()

# 1. Setup Namespaces (Match the 'tei' prefix from your traceback)
results = []
current_book, current_line_num, current_content = None, None, []
ignore_depth = 0
EXCLUDED_TAGS = {"{http://www.tei-c.org/ns/1.0}note", "note", "{http://www.tei-c.org/ns/1.0}bibl", "bibl"}

for event, elem in etree.iterwalk(root, events=("start", "end")):
    tag = elem.tag

    if event == "start":
        if tag.endswith("div") and elem.get("subtype") == "book":
            current_book = elem.get("n")
        elif tag.endswith("milestone") and elem.get("unit") == "line":
            if current_line_num is not None:
                results.append({"book": current_book, "line": current_line_num,
                                "text": " ".join("".join(current_content).split())})
            current_line_num = elem.get("n")
            current_content = []

        if tag in EXCLUDED_TAGS:
            ignore_depth += 1
        elif ignore_depth == 0 and elem.text:
            current_content.append(elem.text)

    elif event == "end":
        # FIXED: Decrement depth BEFORE checking for tail text
        if tag in EXCLUDED_TAGS:
            ignore_depth -= 1

        # If we are now at depth 0, we MUST collect the tail of the element we just closed
        if ignore_depth == 0 and current_line_num is not None and elem.tail:
            current_content.append(elem.tail)


# --- PART 2: FIXED GREEK ALIGNMENT ---
res_list_final = []

for counter, entry in enumerate(results):
    book = int(entry['book'])
    line_start = int(entry['line'])  # e.g., 1
    eng_text = entry['text']

    greek_list = grc_res.get(book, [])

    # 1. Determine the end milestone
    if counter + 1 < len(results) and int(results[counter + 1]['book']) == book:
        line_end = int(results[counter + 1]['line'])  # e.g., 5
    else:
        # If it's the last milestone in the book, go to the very end
        line_end = len(greek_list)

    # 2. ADJUSTED SLICING LOGIC
    # Goal: M1 to M5 captures lines 1, 2, 3, 4, 5 (Indices 0, 1, 2, 3, 4)
    # Goal: M5 to M10 captures lines 6, 7, 8, 9, 10 (Indices 5, 6, 7, 8, 9)

    if line_start == 1:
        start_idx = 0
    else:
        # If line_start is 5, we want to start at index 5 (which is Line 6)
        start_idx = line_start

        # If line_end is 5, slice [:5] captures indices 0, 1, 2, 3, 4
    end_idx = line_end

    greek_segment = greek_list[start_idx:end_idx]
    grc_txt = " ".join(greek_segment).strip()

    res_list_final.append((grc_txt, eng_text))
print(len(grc_res[1]))
#random.seed(42)
#random.shuffle(res_list_final)
with open("test_training.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(res_list_final)