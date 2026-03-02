import csv

with open("/dss/dsshome1/0F/ge64rom2/ancient-greek-datasets/translation_pairs_a.txt", 'r') as f:
    lines=f.readlines()
    res=[(line.split("\t")[0].replace("\n", "").strip(), line.split("\t")[1].replace("\n", "").strip()) for line in lines]
with open("/dss/dsshome1/0F/ge64rom2/ancient-greek-datasets/translation_pairs_b.txt", 'r') as f:
    lines=f.readlines()
    res.extend([(line.split("\t")[0].replace("\n", "").strip(), line.split("\t")[1].replace("\n", "").strip()) for line in lines])
#with open("/dss/dsshome1/0F/ge64rom2/ancient-greek-datasets/translation_pairs_eval.txt", 'r') as f:
#    lines = f.readlines()
#    res.extend([(line.split("\t")[0], line.split("\t")[1]) for line in lines])

with open("grc_eng_training_big.csv", "w") as f:
    writer=csv.writer(f)
    writer.writerows(res)
