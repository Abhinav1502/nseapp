import requests
import json
url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
         'accept-language':'en-US,en;q=0.9,bn;q=0.8','accept-encoding':'gzip, deflate, br'}
r=requests.get(url,headers=headers).json()
with open("data.json", "w") as outfile:
    json.dump(r, outfile)
