import re

input_file="C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\grc-lat.test.lat"

with open(input_file, "r", encoding="utf-8") as f:
    lines=f.readlines()
    print(len(lines))
excluded=[line for line in lines if re.search("[Ͱ-ϡ]+", line)]
print(len(excluded))
lines=[line for line in lines if not re.search("[Ͱ-ϡ]+", line)]
print(len(lines))
lines=[line.replace("j", "i") for line in lines]
whitespace=False
for i, line in enumerate(lines):
    text=""
    for char in line:
        if whitespace and char == " ":
            pass
        elif whitespace and char != " ":
            whitespace=False
            text+=char
        elif not whitespace and char == " ":
            whitespace=True
            text+=char
        else:
            text+=char
    lines[i]=text

with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\corpus_preprocessed\\grc-lat.test.lat", "w", encoding="utf-8") as f:
    f.writelines(lines)