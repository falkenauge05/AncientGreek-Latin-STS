from lxml import etree, html
tree = etree.parse("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristoteles_Med\\hypothesibus_planetarum.xml")
root = tree.getroot()
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
sections=root.findall(".//tei:div2/tei:p", namespaces=ns)
res=""
print(len(sections))
for section in sections:
    for note in section.findall(".//tei:note", namespaces=ns):
        if note.tail:
            prev = note.getprevious()
            if prev is not None:
                prev.tail = (prev.tail or "") + note.tail
            else:
                parent = note.getparent()
                parent.text = (parent.text or "") + note.tail
        note.getparent().remove(note)
    for note in section.findall(".//tei:emph", namespaces=ns):
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
with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristoteles_Med\\out.txt", "w", encoding="utf-8") as f:
    f.write(res)