from lxml import etree, html
tree = etree.parse("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\hippokrates_aphorismoi.xml")
root = tree.getroot()
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
sections=root.findall(".//tei:div[@subtype='chapter']/tei:p", namespaces=ns)
res=""
print(len(sections))
for section in sections:
    for choice in section.findall(".//tei:choice", namespaces=ns):
        corr=choice.find("tei:corr", namespaces=ns)
        corr_text=corr.text if corr is not None else ""
        corr_el=etree.Element("corr")
        corr_el.text=corr_text
        corr_el.tail=choice.tail
        choice.getparent().replace(choice, corr_el)
    for note in section.findall(".//tei:note", namespaces=ns):
        if note.tail:
            prev = note.getprevious()
            if prev is not None:
                prev.tail = (prev.tail or "") + note.tail
            else:
                parent = note.getparent()
                parent.text = (parent.text or "") + note.tail
        note.getparent().remove(note)
    res+="".join(section.itertext())

res=res.replace("\\", "")
res=res.replace("'", "")
with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\out.txt", "w", encoding="utf-8") as f:
    f.write(res)