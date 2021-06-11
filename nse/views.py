from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from .models import NsePE,NseCE
import time
# Create your views here.
import requests
import pandas as pd
import json
def fill(i):
    d = dict.fromkeys(list(i.keys()),0)
    d['strikePrice'] = i['strikePrice']
    d['expiryDate'] = i['expiryDate']
    d['underlying'] = i['underlying']
    d['identifier'] = i['identifier']
    return d

def getNSE(nse,con):
    model_instances =[]
    if con=="pe":
        for _,row in nse.iterrows():
            d = row.tolist()
            model_instances.append(NsePE(strikePrice=d[0],expiryDate=d[1],underlying=d[2],identifier=d[3],openInterest=d[4],changeinOpenInterest=d[5],pchangeinOpenInterest=d[6],totalTradedVolume=d[7],impliedVolatility=d[8],lastPrice=d[9],change=d[10],pChange=d[11],totalBuyQuantity=d[12],totalSellQuantity=d[13],bidQty=d[14],bidprice=d[15],askQty=d[16],askPrice=d[17],underlyingValue=d[18]))
    else:
        for _,row in nse.iterrows():
            d = row.tolist()
            model_instances.append(NsePE(strikePrice=d[0],expiryDate=d[1],underlying=d[2],identifier=d[3],openInterest=d[4],changeinOpenInterest=d[5],pchangeinOpenInterest=d[6],totalTradedVolume=d[7],impliedVolatility=d[8],lastPrice=d[9],change=d[10],pChange=d[11],totalBuyQuantity=d[12],totalSellQuantity=d[13],bidQty=d[14],bidprice=d[15],askQty=d[16],askPrice=d[17],underlyingValue=d[18]))
    return model_instances
def get_data():
    url = 'https://www.NsePEPEindia.com/api/option-chain-indices?symbol=NIFTY'
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
             'accept-language':'en-US,en;q=0.9,bn;q=0.8','accept-encoding':'gzip, deflate, br'}

    data=requests.get(url,headers=headers).json()
    # f = open('data.json',)
    # data = json.load(f)

    try: 
        PE = []
        CE = []
        for i in data["records"]["data"]:
            keys = i.keys()
            if 'PE' in keys and 'CE' in keys:
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
        ce = pd.DataFrame(CE)
        pe = getNSE(pe,'pe')
        ce = getNSE(ce,'ce')
        entries1= NsePE.objects.all()
        entries1.delete()
        entries2  = NseCE.objects.all()
        entries2.delete()
        NsePE.objects.bulk_create(pe)
        NseCE.objects.bulk_create(ce)
        return True
    except(e):
        print(e)
        print("Please try after sometime")
        return False


def get_nsedata(request):
        if request.method == 'GET':
            stat = ""
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            if get_data():
                stat = "Success"
            else:
                stat = "Failed"
            print("Data Fetched at",current_time, "Status :",stat )
            return HttpResponse("Success!")
        else:
            return HttpResponse("Failed!")

def home(request):
    table = ""
    tablePE = NsePE.objects.all()
    tableCE = NseCE.objects.all()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return render(request,'core/home.html',{"tablePE": tablePE,"tableCE":tableCE,"t":current_time})
