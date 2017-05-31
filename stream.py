#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime,timedelta
import sys
import os
import json
import math
# requstsライブラリをインポート
import requests
from requests_oauthlib import OAuth1

def load_arimatsu(name):
    f0 = open("data/{}.dat".format(name),"r")
    txt = f0.readlines()
    f0.close()
    global arimatsu
    arimatsu = float(txt[0].replace("\n",""))
    global arimatsu2
    arimatsu2 = arimatsu

def save_arimatsu(name):
    global arimatsu
    global arimatsu2
    if nosave_mode == 1 and name =="senden_lite":
        arimatsu = arimatsu2
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
nosave_mode = 0

print(res)
print("stream start")
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
                    if add == 9.2: sentence = "@{}\n鉄道で144km移動。7.2アリマツ付与。往復でアリマツを2回通過。2アリマツ付与\n計{}アリマツ".format(tw_data["user"]["screen_name"],arimatsu)
                check = -1
                check = tw_data["text"].find("鉄道アリマツ")
                if check != -1:
                    sindex = tw_data["text"].find("(")
                    findex = tw_data["text"].find(")")
                    if sindex+1 == findex: continue
                    if str(tw_data["text"][sindex+1:findex]).find("*2") != -1:
                        findex = tw_data["text"].find("*2")
                        add = round((float(tw_data["text"][sindex+1:findex])*2)/10,2)
                    elif str(tw_data["text"][sindex+1:findex]).count("+") != 0:
                        count_plus = str(tw_data["text"][sindex+1:findex]).count("+")
                        findex = tw_data["text"].find("+")
                        add = round(float(tw_data["text"][sindex+1:findex])/10,2)
                        for i in range(count_plus):
                            sindex = findex
                            findex = tw_data["text"].find("+", findex + 1)
                            if findex == -1:
                                findex = tw_data["text"].find(")")
                            add += round(float(tw_data["text"][sindex+1:findex])/10,2)
                    else:
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
                    if add >= 1145148101920: continue
                    if add <= -1145148101920: continue
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(arimatsu + add,2)
                    sentence = "@{}\n{}アリマツ付与。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],add,arimatsu)
                check = -1
                check = tw_data["text"].find("ニューアリマツ")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(arimatsu - 50,2)
                    sentence = "@{}\nニューアリマツ建造。50アリマツ消費。\n残り{}アリマツ。".format(tw_data["user"]["screen_name"],arimatsu)
                    if arimatsu < 0:
                        arimatsu += 50
                        sentence = "@{}\nアリマツ不足です。50以上アリマツがあるときに建造してください".format(tw_data["user"]["screen_name"])
                check = -1
                check = tw_data["text"].find("アリマツ確認")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    sentence = "@{}\n{}の現在所持：{}アリマツ".format(tw_data["user"]["screen_name"],tw_data["user"]["screen_name"],arimatsu)
                check = -1
                check = tw_data["text"].find("レポートアリマツ")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(arimatsu + 5,2)
                    sentence = "@{}\nレポートアリマツ5アリマツ付与。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],arimatsu)
                check = -1
                check = tw_data["text"].find("バイトアリマツ")
                if check != -1:
                    sindex = tw_data["text"].find("(")
                    findex = tw_data["text"].find(")")
                    if sindex+1 == findex: continue
                    add = round(math.log10(float(tw_data["text"][sindex+1:findex])),2)
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(arimatsu + add,2)
                    sentence = "@{}\nバイトアリマツ{}付与。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],add,arimatsu)
                check = -1
                check = tw_data["text"].find("arimatsuset")
                if check != -1:
                    sindex = tw_data["text"].find("(")
                    findex = tw_data["text"].find(")")
                    if sindex+1 == findex: continue
                    add = round(float(tw_data["text"][sindex+1:findex]),2)
                    load_arimatsu(tw_data["user"]["screen_name"])
                    arimatsu = round(add,2)
                    sentence = "@{}\narimatsu set.".format(tw_data["user"]["screen_name"])
                check = -1
                check = tw_data["text"].find("ただいま")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    if tw_data["user"]["screen_name"] == "senden_lite": add = 2.54
                    elif tw_data["user"]["screen_name"] == "coppupan_lrc": add = 9.2
                    elif tw_data["user"]["screen_name"] == "ChyMzkP": add = 0
                    arimatsu = round(arimatsu + add,2)
                    sentence = "@{} おかえりなさい。\n鉄道で{}km移動。{}アリマツ付与。\n計{}アリマツ。".format(tw_data["user"]["screen_name"],add*10,add,arimatsu)
                    if add == 9.2: sentence = "@{} おかえりなさい。\n鉄道で144km移動。7.2アリマツ付与。往復でアリマツを2回通過。2アリマツ付与\n計{}アリマツ".format(tw_data["user"]["screen_name"],arimatsu)
                check = -1
                check = tw_data["text"].find("nosave")
                if check != -1 and tw_data["user"]["screen_name"] == "senden_lite":
                    load_arimatsu(tw_data["user"]["screen_name"])
                    nosave_mode += 1
                    if nosave_mode >= 2: nosave_mode = 0
                    stat = "on"
                    if nosave_mode == 0: stat = "off"
                    sentence = "@{}\nnosave_mode is now {}".format(tw_data["user"]["screen_name"],stat)
                check = -1
                check = tw_data["text"].find("生きてる")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    sentence = "@{}\n（ ゜□ﾟ)＜せいぞん、せんりゃくうううううううう！！\nイマージーン！\nきっと何者にもなれないお前たちに告げる！\nhttp://nico.ms/sm24877123\n{}".format(tw_data["user"]["screen_name"],datetime.now().strftime("%s"))
                check = -1
                check = tw_data["text"].find("生存戦略")
                if check != -1:
                    load_arimatsu(tw_data["user"]["screen_name"])
                    sentence = "@{}\n（ ゜□ﾟ)＜せいぞん、せんりゃくうううううううう！！\nイマージーン！\nきっと何者にもなれないお前たちに告げる！\nhttp://nico.ms/sm24877123\n{}".format(tw_data["user"]["screen_name"],datetime.now().strftime("%s"))






                if sentence != "":
                    data = {"status":sentence,"in_reply_to_status_id":tw_data["id_str"]}
                    res2 = requests.post(update_url, data=data, auth=auth)
                    save_arimatsu(tw_data["user"]["screen_name"])
        except (KeyError, ValueError):
            pass
