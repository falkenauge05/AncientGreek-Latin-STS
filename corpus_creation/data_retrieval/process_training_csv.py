import csv
import random

with open("training.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows=list(reader)
    rows=[r for r in rows if len(r.split(" "))>=4]
    random.seed(42)
    random.shuffle(rows)
with open("training.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)