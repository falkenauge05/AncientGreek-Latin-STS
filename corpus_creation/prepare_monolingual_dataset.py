import os
import numpy as np

directory = os.fsencode("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\GREEK")

res_dict={}
output_line_list=[]

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        with open(os.path.join(os.fsdecode(directory), filename), encoding="utf-8") as f:
            lines=f.readlines()
            lines=[line for line in lines if 10<len(line.split(" "))<90]
            res_dict[filename]=len(lines)
            output_line_list.extend(lines)
    else:
        continue
print(res_dict)
print(len(output_line_list))
print(np.mean([len(s.split(" ")) for s in output_line_list]))
#with open("C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Monolingual_BUCC\\result_latin.txt", "w", encoding="utf-8") as f:
#    f.write("".join(output_line_list))