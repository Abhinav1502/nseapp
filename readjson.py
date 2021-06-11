import json
import pandas as pd
# Opening JSON file
f = open('data.json',)

# returns JSON object as
# a dictionary
def fill(i):
    d = dict.fromkeys(list(i.keys()),0)
    d['strikePrice'] = i['strikePrice']
    d['expiryDate'] = i['expiryDate']
    d['underlying'] = i['underlying']
    d['identifier'] = i['identifier']
    return d
PE = []
CE = []
data = json.load(f)
exp_dates = data['records']['expiryDates']
for i in data["records"]["data"]:
    keys = i.keys()
    if 'PE' in keys and'CE' in keys:
        PE.append(i['PE'])
        CE.append(i['CE'])
    else:
        if 'PE' in keys:
            PE.append(i['PE'])
            dd = fill(i['PE'])
            CE.append(dd)
        else:
            CE.append(i['CE'])
            dd = fill(i['CE'])
            PE.append(dd)
pe = pd.DataFrame(PE)
pe = pe[:5]
ce = pd.DataFrame(CE)
print(pe.columns)
for _,row in pe.iterrows():
    d = row.tolist()
    print(d[0],d[1])
# Closing file
f.close()
