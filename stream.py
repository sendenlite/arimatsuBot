#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime,timedelta
import sys
import os
import json
# requstsライブラリをインポート
import requests
from requests_oauthlib import OAuth1

def load_arimatsu(name):
    f0 = open("data/{}.dat".format(name),"r")
    txt = f0.readlines()
    f0.close()
    global arimatsu
    arimatsu = float(txt[0].replace("\n",""))

def save_arimatsu(name):
    f1 = open("data/{}.dat".format(name),"w")
    f1.write(str(arimatsu))
    f1.close()

userid = "bdbdbot"

count = 0
for line in open("data/CONSUMER.dat","r"):

    if count == 0:
        CONSUMER_KEY = str(line.rstrip())
    if count == 1:
        CONSUMER_SECRET = str(line.rstrip())
    count += 1

count = 0
for line in open("data/{}.verify".format(userid),"r"):

    if count == 0:
        ACCESS_TOKEN = str(line.rstrip())
    if count == 1:
        ACCESS_SECRET = str(line.rstrip())
    count += 1

auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

timeline_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
update_url =  "https://api.twitter.com/1.1/statuses/update.json"
streaming_url = "https://userstream.twitter.com/1.1/user.json"

data = {}
res = requests.post(streaming_url, auth=auth, stream=True, data=data)

print(res)
print("steam start")
for line in res.iter_lines():
    if line:
        decoded_line = line.decode('utf-8')
        tw_data = json.loads(decoded_line)
        try:        
            if tw_data["in_reply_to_screen_name"] == "bdbdbot":
                if os.path.exists("data/{}.dat".format(tw_data["user"]["screen_name"])):
                    pass
                else:
                    continue
                print(tw_data)
                sentence = ""
                check = -1
                check = tw_data["text"].find("通学アリマツ")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    if tw_data["user"]["screen_name"] == "senden_lite": add = 2.54
                    elif tw_data["user"]["screen_name"] == "coppupan_lrc": add = 9.2
                    elif tw_data["user"]["screen_name"] == "ChyMzkP": add = 0
                    arimatsu = round(arimatsu + add,2)
                    sentence = "@{}\n鉄道で{}km移動。{}アリマツ付与。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],add*10,add,arimatsu)
                    if add ==9.2: sentence = "@{}\n鉄道で14.4km移動。7.2アリマツ付与。往復でアリマツを2回通過。2アリマツ付与\n計{}アリマツ".format(tw_data["user"]["screen_name"])
                check = -1
                check = tw_data["text"].find("鉄道アリマツ")
                if check != -1:
                    sindex = tw_data["text"].find("(")
                    findex = tw_data["text"].find(")")
                    if sindex+1 == findex: continue
                    add = round(float(tw_data["text"][sindex+1:findex])/10,2)
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(arimatsu + add,2)
                    sentence = "@{}\n鉄道で{}km移動。{}アリマツ付与。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],add*10,add,arimatsu)
                check = -1
                check = tw_data["text"].find("アリマツ付与")
                if check != -1:
                    sindex = tw_data["text"].find("(")
                    findex = tw_data["text"].find(")")
                    if sindex+1 == findex: continue
                    add = round(float(tw_data["text"][sindex+1:findex]),2)
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(arimatsu + add,2)
                    sentence = "@{}\n{}アリマツ付与。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],add,arimatsu)
                check = -1
                check = tw_data["text"].find("ニューアリマツ")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(arimatsu - 50,2)
                    sentence = "@{}\nニューアリマツ建造。50アリマツ消費。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],arimatsu)




                if sentence != "":
                    data = {"status":sentence,"in_reply_to_status_id":tw_data["id_str"]}
                    res2 = requests.post(update_url, data=data, auth=auth)
                    save_arimatsu(tw_data["user"]["screen_name"])
        except (KeyError, ValueError):
            pass
