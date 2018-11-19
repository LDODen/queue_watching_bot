import os
import json

qsett_array = []
with open("qsett.txt", "r") as qsett:
    for ln in qsett:
        qsett_array.append(ln.strip())

sett_array = []        
with open("sett.txt", "r") as sett:
    for ln in sett:
        sett_array.append(ln.strip())
    
print(qsett_array)
print(sett_array)

with open("set.json", "r") as sett:
    jfile = json.loads(sett.read())

print(jfile["host"])