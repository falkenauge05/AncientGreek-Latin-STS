from lxml import etree
import csv

# Load TEI XML
tree = etree.parse("hippokrates.xml")

# TEI namespace
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# XPath to all aphorism divs
aphorisms = tree.xpath(
    "/tei:TEI/tei:text/tei:body/tei:div/tei:div/tei:div",
    namespaces=NS
)

results = []

for aph in aphorisms:
    aph_num = aph.get("n")
    section = aph.getparent().get("n")

    text = " ".join(
        aph.xpath(".//tei:p//text()", namespaces=NS)
    ).strip()

    results.append({
        "section": section,
        "aphorism": aph_num,
        "text": text
    })

with open("hippokrates.csv", 'w') as csvfile:
    csv.writer(csvfile).writerows([[res['section']+"."+res['aphorism'], res['text']] for res in results])
