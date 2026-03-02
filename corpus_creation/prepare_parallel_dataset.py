import pathlib
import random
directory=pathlib.Path("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristoteles Analytica Priora")
directory2=pathlib.Path("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristotle Topica")
directory3="C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Vulgata_Septuaginta\\"
directory4="C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Timaeus\\"


files=list(directory.rglob("*lat.txt"))


line_list=[]
for file in files:
    with open(file, encoding="utf-8") as f:
        with open(str(file).replace("lat.txt", "gre.txt"), encoding="utf-8") as f2:
            lines_lat=f.readlines()
            lines_grc=f2.readlines()
            lines=[(lines_grc[i], line_lat) for i, line_lat in enumerate(lines_lat) if 10<len(line_lat.split(" "))<90]
            line_list.extend(lines)
files=list(directory2.rglob("*lat.txt"))
for file in files:
    with open(file, encoding="utf-8") as f:
        with open(str(file).replace("lat.txt", "gre.txt"), encoding="utf-8") as f2:
            lines_lat=f.readlines()
            lines_grc=f2.readlines()
            lines=[(lines_grc[i], line_lat) for i, line_lat in enumerate(lines_lat) if len(line_lat.split(" "))>10 and len(line_lat.split(" "))<90]
            line_list.extend(lines)
random.seed(42)
line_list=random.sample(line_list, 1000)
with open(directory3+"out_lat.txt", encoding="utf-8") as f:
    with open(directory3+"out_grc.txt", encoding="utf-8") as f2:
        lines_lat=f.readlines()
        lines_grc=f2.readlines()
        lines=[(lines_grc[i], line_lat) for i, line_lat in enumerate(lines_lat) if len(line_lat.split(" "))>10 and len(line_lat.split(" "))<90]
#new testament
line_list.extend(random.sample(lines, 1000))
with open(directory4+"Calcidius_gre.txt", encoding="utf-8") as f:
    with open(directory4+"Calcidius_lat.txt", encoding="utf-8") as f2:
        lines_lat=f.readlines()
        lines_grc=f2.readlines()
        lines=[(lines_grc[i], line_lat) for i, line_lat in enumerate(lines_lat) if 10<len(line_lat.split(" "))<90]
line_list.extend(lines)
print(len(line_list))
with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\parallel_latin2.txt", "w", encoding="utf-8") as f:
    f.writelines(line_lat if line_lat.endswith("\n") else line_lat + "\n" for _, line_lat in line_list)
with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\parallel_greek2.txt", "w", encoding="utf-8") as f:
    f.writelines(line_grc if line_grc.endswith("\n") else line_grc + "\n" for line_grc, _ in line_list)
with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\parallel_latin2.txt", "r", encoding="utf-8") as f:
    print(len(f.readlines()))
with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\parallel_greek2.txt", "r", encoding="utf-8") as f:
    print(len(f.readlines()))