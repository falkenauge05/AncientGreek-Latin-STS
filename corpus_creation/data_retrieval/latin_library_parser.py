from bs4 import BeautifulSoup, NavigableString

# Load the HTML file
with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\Sidonius_ Epistularum Liber I.html", "r", encoding="windows-1252") as f:
    soup = BeautifulSoup(f, "html.parser")

# Collect all desired text
# texts = []
# for p in soup.find_all("p"):
#     # Skip <p> with nested tags that aren't simple inline (like <table>)
#     #if any(child.name not in {None, 'b'} for child in p.descendants if hasattr(child, "name")):
#     #    continue
#     # Remove bold sections
#     for b in p.find_all("b"):
#         b.extract()
#     # Get remaining text (strip whitespace)
#     text = p.get_text(strip=True)
#     if text:
#         texts.append(text)
texts = []
for p in soup.find_all("p"):
    # Collect only direct text (not nested inside other tags)
    direct_text = ''.join(
        t for t in p.contents if isinstance(t, NavigableString)
    ).strip()

    if direct_text:
        texts.append(direct_text)

# Join all the extracted text
result = " ".join(texts)

real_result=""
whitespace=False
point=False
skip=False
for i, c in enumerate(result):
    if c=="[" and result[i+1].isdigit():
        skip=True
    elif c=="]":
        skip=False
    elif not skip:
        if c==" " and not whitespace:
            real_result+=c
            whitespace=True
        elif c!=" ":
            whitespace=False
            if c!="'":
                if c.isdigit() and result[i+1]==".":
                    point=True
                elif point:
                    point=False
                else:
                    real_result+=c

with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\out.txt", "w", encoding="utf-8") as out:
    out.write(real_result)
