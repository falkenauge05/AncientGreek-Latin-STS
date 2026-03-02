input_file="C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Timaeus\\Calidius\\timaeus parallel.html"
output_file="C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Timaeus\\Calidius\\output.txt"

with open(input_file, 'r', encoding='utf-8') as f:
    text=f.readlines()

number_sentences=0
last_font_was_latin=False

for line in text:
    if "<font color='#006600'" in line and not last_font_was_latin:
        number_sentences+=1
        last_font_was_latin=True
    elif "<font color='#000099'" in line:
        last_font_was_latin=False
print(number_sentences)