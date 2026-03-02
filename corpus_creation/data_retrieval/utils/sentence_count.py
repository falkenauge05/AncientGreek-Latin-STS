filename="C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Clemens Romanus (Pseudo) Epistula ad Iacobum\\"
number_sentences=0
for i in range(1, 21):
    with open(filename+str(i)+"_gre.txt", "r", encoding="utf-8") as f:
        length=len(f.readlines())
        number_sentences+=length
        greek_sent_number=length
    with open(filename+str(i)+"_lat.txt", "r", encoding="utf-8") as f:
        if len(f.readlines())!=greek_sent_number:
            print("Sentence numbers differ: "+str(i))


print(number_sentences)