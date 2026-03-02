import requests
from bs4 import BeautifulSoup
import csv
import re
import unicodedata

url = "https://www.logicmuseum.com/wiki/Authors/Aristotle/de_anima/L3"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; example script)"
}

resp = requests.get(url, headers=headers)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")

def clean_cell(cell):
    """
    Remove <a> tags *and their text*, then extract plain text.
    """
    for a in cell.find_all("a"):
        a.decompose()       # removes the tag AND the text inside it
    return cell.get_text(" ", strip=True)

def extract_plaintext_table(table):
    first_row = table.find("tr")
    if not first_row:
        return None

    headers = [th.get_text(strip=True) for th in first_row.find_all(["th", "td"])]
    if "Greek" not in headers or "Latin" not in headers:
        return None

    greek_i = headers.index("Greek")
    latin_i = headers.index("Latin")

    rows = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if not cells:
            continue

        greek_text = clean_cell(cells[greek_i]) if greek_i < len(cells) else ""
        latin_text = clean_cell(cells[latin_i]) if latin_i < len(cells) else ""

        rows.append((greek_text, latin_text))

    return rows


final_list=[]
# Find the correct table
for table in soup.find_all("table"):
    result = extract_plaintext_table(table)
    if result is not None:
        for greek, latin in result:
            if greek != "" and 10<len(greek.split(" "))<100:
                greek=re.sub(r"([0-9]+[.])", "", greek)
                greek=re.sub(r"(\[[0-9]])", "", greek)
                greek=re.sub(r" +", " ", greek)
                latin=re.sub(r"([0-9]+[.])", "", latin)
                latin=re.sub(r"(\[[0-9]])", "", latin)
                latin=re.sub(r" +", " ", latin)
                greek=greek.strip()
                latin=latin.strip()
                greek=unicodedata.normalize("NFC", greek)
                latin=unicodedata.normalize("NFC", latin)
                final_list.append((greek, latin))

print(len(final_list))

with open("de_anima.csv", 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(final_list)