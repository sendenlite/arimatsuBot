#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime,timedelta
import sys
import os
import json
import math
from time import sleep
from janome.tokenizer import Tokenizer
import re
import random
# requstsライブラリをインポート
import requests
from requests_oauthlib import OAuth1

class Arimatsu:

    reply_id = ""
    timeline_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    update_url =  "https://api.twitter.com/1.1/statuses/update.json"
    streaming_url = "https://userstream.twitter.com/1.1/user.json"
    mention_url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

    def __init__(self,mode_flag=0,nosave_mode=0):
        self.mode_flag = mode_flag
        self.nosave_mode = nosave_mode
        userid = "bdbdbot"
        if self.mode_flag==0:
            self.t=Tokenizer()
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
        
        self.auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        pattern = r"^@bdbdbot\s+(\d)[Dd](\d+)"
        self.repatter = re.compile(pattern)

    def loadArimatsu(self,name):
        f0 = open("data/{}.dat".format(name),"r")
        txt = f0.readlines()
        f0.close()
        self.arimatsu = float(txt[0].replace("\n",""))
        self.arimatsu2 = self.arimatsu
    
    def saveArimatsu(self,name,nosave=False):
        if (self.nosave_mode == 1 and name =="senden_lite") or nosave:
            self.arimatsu = self.arimatsu2
        f1 = open("data/{}.dat".format(name),"w")
        f1.write(str(self.arimatsu))
        f1.close()

    def arimatsuManList(self):
        self.files  = []
        self.men  = []
        self.files = os.listdir('/home/kohki/arimatsu/data/') 
        self.files.remove('CONSUMER.dat')
        for fil in self.files:
            if fil.find('.dat')!=-1:
                self.men.append(fil[0:-4])

    def haifu(self,main_name,text): 
        if main_name != "senden_lite" and main_name !="coppupan_lrc":
            return
        sindex = text.find("(")
        findex = text.find(")")
        if sindex+1 == findex: return
        add = round(float(text[sindex+1:findex]),2)
        if add >= 1145148101920: return
        if add <= -1145148101920: return
        self.arimatsuManList()
        sentence = "@{}\n{}アリマツ配布！\n現在アリマツ\n".format(main_name,round(add,5))
        for name in self.men:
            self.loadArimatsu(name)
            self.arimatsu = round(self.arimatsu + add,2)
            sentence += "@{} : {}\n".format(name,self.arimatsu)
            if self.nosave_mode == 1 and main_name == "senden_lite":
                self.saveArimatsu(name,nosave=True)
            else:
                self.saveArimatsu(name)
        self.tweet(sentence,main_name,save=False)


    def tsugaku(self,name):
        self.loadArimatsu(name)
        if name == "senden_lite": add = 2.54
        elif name == "coppupan_lrc": add = 9.2
        elif name == "ChyMzkP": add = 0
        self.arimatsu = round(self.arimatsu + add,2)
        sentence = "@{}\n鉄道で{}km移動。{}アリマツ付与。\n計{}アリマツ。".format(name,add*10,add,self.arimatsu)
        if add == 9.2: sentence = "@{}\n鉄道で144km移動。7.2アリマツ付与。往復でアリマツを2回通過。2アリマツ付与\n計{}アリマツ".format(name,arimatsu)
        self.addHistory(name,"{} > {}アリマツ付与(通学アリマツ)".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(add,5)))
        self.tweet(sentence,name)

    def tetsudou(self,name,text):
        twice_flag = 0
        sindex = text.find("(")
        findex = text.find(")")
        if sindex+1 == findex: return
        if str(text[sindex+1:findex]).find("*2") != -1:
            findex = text.find("*2")
            twice_flag = 1
        if str(text[sindex+1:findex]).count("+") != 0:
            count_plus = str(text[sindex+1:findex]).count("+")
            findex = text.find("+")
            add = round(float(text[sindex+1:findex])/10,2)
            for i in range(count_plus):
                sindex = findex
                findex = text.find("+", findex + 1)
                if findex == -1:
                    if twice_flag == 1:
                        findex = text.find("*2")
                    else:
                        findex = text.find(")")
                add += round(float(text[sindex+1:findex])/10,2)
        else:
            add = round(float(text[sindex+1:findex])/10,2)
        if twice_flag == 1:
            add *= 2
        self.loadArimatsu(name)
        self.arimatsu = round(self.arimatsu + add,2)
        sentence = "@{}\n鉄道で{}km移動。{}アリマツ付与。\n計{}アリマツ。".format(name,round(add*10,5),add,self.arimatsu)
        self.addHistory(name,"{} > {}アリマツ付与(鉄道アリマツ)".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(add,5)))
        self.tweet(sentence,name)

    def fuyo(self,name,text):
        sindex = text.find("(")
        findex = text.find(")")
        if sindex+1 == findex: return
        add = round(float(text[sindex+1:findex]),2)
        if add >= 1145148101920: return
        if add <= -1145148101920: return
        self.loadArimatsu(name)
        self.arimatsu = round(self.arimatsu + add,2)
        sentence = "@{} {}アリマツ付与。\n計{}アリマツ。".format(name,round(add,5),self.arimatsu)
        self.addHistory(name,"{} > {}アリマツ付与".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(add,5)))
        self.tweet(sentence,name)

    def new(self,name,text):
        self.loadArimatsu(name)
        self.arimatsu = round(self.arimatsu - 50,2)
        sentence = "@{}\nニューアリマツ建造。50アリマツ消費。\n残り{}アリマツ。".format(name,self.arimatsu)
        if self.arimatsu < 0:
            self.arimatsu += 50
            sentence = "@{}\nアリマツ不足です。50以上アリマツがあるときに建造してください".format(name)
        self.addHistory(name,"{} > ニューアリマツ建造".format(datetime.now().strftime('%Y/%m/%d %H:%M')))
        self.tweet(sentence,name)

    def kakunin(self,name):
        self.loadArimatsu(name)
        sentence = "@{}\n{}の現在所持：{}アリマツ".format(name,name,self.arimatsu)
        self.tweet(sentence,name)

    def report(self,name):
        self.loadArimatsu(name)
        self.arimatsu = round(self.arimatsu + 5,2)
        sentence = "@{}\nレポートアリマツ5アリマツ付与。\n計{}アリマツ。".format(name,self.arimatsu)
        self.addHistory(name,"{} > {}アリマツ付与(レポートアリマツ)".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(5,5)))
        self.tweet(sentence,name)


    def ohayo(self,name):
        self.loadArimatsu(name)
        self.arimatsu = round(self.arimatsu + 5,2)
        replies = ['おはよう！','おはようございます。','おはよおおおおお\nこんちはああああ\nこんばんはあああ\nおやすみいいいい\n起きてぇぇぇぇぇえええええ！','おはよー！！！起きて！！！朝だよ！！！すごい朝！！！外が明るい！！！！カンカンカンカンカンカンカンカンカンカンカンカン！！！おはよ！！！見て見て！！！外明るいの！！！外！！！！見て！！！カンカンカン！！！','おはよう^^','おはよう','おはようございます。','Good morning!','Guten Morgen.','おはようなの',]
        if name == 'ChyMzkP': replies += ['早上好','早上好','早上好','早上好','早上好'] 
        addSentence = ''
        if datetime.now().hour >= 14: addSentence = 'もう昼過ぎだゾ\n' 
        elif datetime.now().hour <= 4: addSentence = '朝早スギィ！！\n'
        sentence = "@{}\n{}\n{}5アリマツ付与。\n計{}アリマツ。".format(name,random.choice(replies),addSentence,self.arimatsu)
        if len(sentence) >= 140: sentence = "@{}\n{}\n5アリマツ付与。\n計{}アリマツ。".format(name,random.choice(replies),self.arimatsu)
        self.addHistory(name,"{} > {}アリマツ付与(おはようアリマツ)".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(5,5)))
        self.tweet(sentence,name)


    def baito(self,name,text):
        sindex = text.find("(")
        findex = text.find(")")
        if sindex+1 == findex: return
        add = round(math.log10(float(text[sindex+1:findex])),2)
        self.loadArimatsu(name)
        self.arimatsu = round(self.arimatsu + add,2)
        sentence = "@{}\nバイトアリマツ{}付与。\n計{}アリマツ。".format(name,add,self.arimatsu)
        self.addHistory(name,"{} > {}アリマツ付与(バイトアリマツ)".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(add,5)))
        self.tweet(sentence,name)

    def setArimatsu(self,name,text):
        sindex = text.find("(")
        findex = text.find(")")
        if sindex+1 == findex: return
        add = round(float(text[sindex+1:findex]),2)
        self.loadArimatsu(name)
        self.arimatsu = round(add,2)
        sentence = "@{}\narimatsu set.".format(name)
        self.addHistory(name,"{} > {}アリマツset".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(add,5)))
        self.tweet(sentence,name)

    def tadaima(self,name,text):
        self.loadArimatsu(name)
        if name == "senden_lite": add = 2.54
        elif name == "coppupan_lrc": add = 9.2
        elif name == "ChyMzkP": add = 0
        self.arimatsu = round(self.arimatsu + add,2)
        tokens = self.t.tokenize(text)
        keiyou = 0
        wakaru = ""
        for token in tokens:
            partOfSpeech = token.part_of_speech.split(",")[0]
            if partOfSpeech == "形容詞":
                keiyou += 1
                keiyoushi = token.surface
            if keiyou == 1:
                wakaru = "わかる{}い\n".format(keiyoushi[0:-1])
        sentence = "@{} おかえりなさい。\n{}鉄道で{}km移動。{}アリマツ付与。\n計{}アリマツ。".format(name,wakaru,add*10,add,self.arimatsu)
        if add == 9.2: sentence = "@{} おかえりなさい。\n{}鉄道で144km移動。7.2アリマツ付与。往復でアリマツを2回通過。2アリマツ付与\n計{}アリマツ".format(name,wakaru,self.arimatsu)
        self.addHistory(name,"{} > {}アリマツ付与(通学アリマツ)".format(datetime.now().strftime('%Y/%m/%d %H:%M'),round(add,5)))
        self.tweet(sentence,name)

    def nosave(self,name):
        self.loadArimatsu(name)
        self.nosave_mode += 1
        if self.nosave_mode >= 2: self.nosave_mode = 0
        stat = "on"
        if self.nosave_mode == 0: stat = "off"
        sentence = "@{}\nnosave_mode is now {}".format(name,stat)
        self.tweet(sentence,name)

    def seizon(self,name):
        sentence = "@{}\n（ ゜□ﾟ)＜せいぞん、せんりゃくうううううううう！！\nイマージーン！\nきっと何者にもなれないお前たちに告げる！\nhttp://nico.ms/sm24877123\n{}".format(name,datetime.now().strftime("%s"))
        self.tweet(sentence,name,save=False)

    def getHistory(self,name):
        hfile = open("data/{}.history".format(name),"r")
        histories = ("@{}\n".format(name))+hfile.read()
        self.tweet(histories,name,save=False)

    def addHistory(self,name,sentence):
        hfile = open("data/{}.history".format(name),"r")
        histories = hfile.readlines()
        histories = "".join(["{}\n".format(sentence)]+histories[0:4])
        hfile = open("data/{}.history".format(name),"w")
        hfile.write(histories)

    def dice(self,name,amount,size):
        dd = []
        for i in range(int(amount)):
            d = random.randint(1,int(size))
            dd.append(d)
        sentence = "@{}\n[ {} ]\n計{}".format(name," ".join(list(map(str,dd))),sum(dd))
        self.tweet(sentence,name,save=False)

    def tweet(self,sentence,name,save=True):
        if sentence != "":
            if self.nosave_mode == 1 and name == "senden_lite":
                sentence += "(nosave)"
            data = {"status":sentence,"in_reply_to_status_id":self.tw_data["id_str"]}
            if self.reply_id != "":
                data = {"status":sentence,"in_reply_to_status_id":self.reply_id}
                self.reply_id = ""   
            res2 = requests.post(self.update_url, data=data, auth=self.auth)
            if save:
                self.saveArimatsu(name)

    def listen(self):
        data = {}
        self.res = requests.post(self.streaming_url, auth=self.auth, stream=True, data=data)
        print(self.res)
        print("stream start")

        for line in self.res.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                self.tw_data = json.loads(decoded_line)
                try:        
                    if self.tw_data["in_reply_to_screen_name"] == "bdbdbot":
                        if os.path.exists("data/{}.dat".format(self.tw_data["user"]["screen_name"])):
                            print(self.tw_data)
        
                            check = -1
                            check = self.tw_data["text"].find("通学アリマツ")
                            if check != -1:
                                self.tsugaku(self.tw_data["user"]["screen_name"])
                            check = -1
        
                            check = self.tw_data["text"].find("鉄道アリマツ")
                            if check != -1:
                                self.tetsudou(self.tw_data["user"]["screen_name"],self.tw_data["text"])
                            check = -1
        
                            check = self.tw_data["text"].find("アリマツ付与")
                            if check != -1:
                                self.fuyo(self.tw_data["user"]["screen_name"],self.tw_data["text"])
                            check = -1

                            check = self.tw_data["text"].find("アリマツ配布")
                            if check != -1:
                                self.haifu(self.tw_data["user"]["screen_name"],self.tw_data["text"])
                            check = -1
        
                            check = self.tw_data["text"].find("ニューアリマツ")
                            if check != -1:
                                self.new(self.tw_data["user"]["screen_name"],self.tw_data["text"])
                            check = -1
        
                            check = self.tw_data["text"].find("アリマツ確認")
                            if check != -1:
                                self.kakunin(self.tw_data["user"]["screen_name"])
                            check = -1
        
                            check = self.tw_data["text"].find("レポートアリマツ")
                            if check != -1:
                                self.report(self.tw_data["user"]["screen_name"])
                            check = -1
        
                            check = self.tw_data["text"].find("バイトアリマツ")
                            if check != -1:
                                self.baito(self.tw_data["user"]["screen_name"],self.tw_data["text"])
                            check = -1
        
                            check = self.tw_data["text"].find("arimatsuset")
                            if check != -1:
                                self.setArimatsu(self.tw_data["user"]["screen_name"],self.tw_data["text"])
                            check = -1
        
                            check = self.tw_data["text"].find("ただいま")
                            if check != -1:
                                self.tadaima(self.tw_data["user"]["screen_name"],self.tw_data["text"])
                            check = -1
        
                            check = self.tw_data["text"].find("nosave")
                            if check != -1 and self.tw_data["user"]["screen_name"] == "senden_lite":
                                self.nosave(self.tw_data["user"]["screen_name"])
                            check = -1
        
                            check = self.tw_data["text"].find("生きてる")
                            if check != -1:
                                self.seizon(self.tw_data["user"]["screen_name"])
                            check = -1
        
                            check = self.tw_data["text"].find("生存戦略")
                            if check != -1:
                                self.seizon(self.tw_data["user"]["screen_name"])
                            check = -1

                            m = self.repatter.search(self.tw_data["text"])
                            if m:
                                self.dice(self.tw_data["user"]["screen_name"],m.group(1),m.group(2))

                            check = self.tw_data["text"].find("アリマツ履歴")
                            if check != -1:
                                self.getHistory(self.tw_data["user"]["screen_name"])
                            check = -1

                            check = self.tw_data["text"].find("おはよ")
                            if check != -1:
                                self.ohayo(self.tw_data["user"]["screen_name"])
                            check = -1


        
#                            if self.tw_data["text"][0:16] == "@bdbdbot python:" or self.tw_data["text"][0:11] == "@bdbdbot c:":
#                                arimatsu.loadArimatsu(self.tw_data["user"]["screen_name"])
#                                sentence = "@paiza_run"+self.tw_data["text"][8:]
#                                data = {"status":sentence}
#                                res2 = requests.post(update_url, data=data, auth=auth)
#                                sleep(3)
#                                params = {"count":2}
#                                res3 = requests.get(mention_url, params=params,  auth=auth)
#                                status_list = res3.json()
#                                for status in status_list:
#                                    sentence = "@paiza_run @{}".format(self.tw_data["user"]["screen_name"])
#                                    if status["user"]["screen_name"] == "paiza_run":
#                                        reply_id = status["id_str"]
 
                except (KeyError, ValueError):
                    pass


