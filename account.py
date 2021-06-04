import json
import io
import os
from glob import glob
import datetime
from datetime import datetime, timedelta, timezone
import discord

class AccountManager:
    def __init__(self):
        self.accounts={}
        pathes = glob('./accounts/**.json')
        for path in pathes:
            with open(path, mode='rt', encoding='utf-8') as file:
                dic = json.load(file)
                acc=Account()
                acc.read(dic)
                self.accounts[acc.id]=acc
    def get_account(self,id):
        if len(self.accounts)==0:return None
        if id not in self.accounts:return None
        return self.accounts[id]
    def save_data(self,id):
        if not self.exists(id): 
            self.accounts[id]=Account()
            self.accounts[id].id=id
        if not os.path.exists("accounts"):#
            print("ディレクトリがありません")
            os.mkdir("accounts")
        with open(f'./accounts/{id}.json', mode='wt', encoding='utf-8') as file:
             json.dump(self.accounts[id].to_data(), file, ensure_ascii=False, indent=2)
    def add(self,id,name):
        if  self.exists(id):return
        self.accounts[id]=Account()
        self.accounts[id].id=id
        self.accounts[id].name=name
    def delete_data(self,id,data): self.accounts.pop(id)
    def exists(self,id):
        if len(self.accounts)==0:return False
        return id in self.accounts.keys()
    def on_status_update(self,before,after):
        id=before.id
        if not self.exists(id):self.add(id,before.name)
        ac=self.accounts[id]        
        now=self.get_now()
        if before.mobile_status!=after.mobile_status and after.mobile_status==discord.Status.offline: ac.last_moblie_active=now
        if before.desktop_status!=after.desktop_status and after.desktop_status==discord.Status.offline: ac.last_desktop_active=now
        if before.web_status!=after.web_status and after.web_status==discord.Status.offline:ac.last_web_active=now
        self.save_data(id)
    def on_message(self,message):
        id=message.author.id
        if not self.exists(id):self.add(id,message.author.name)
        ac=self.accounts[id]
        now=self.get_now()
        ac.last_message=message.content
        ac.message_count+=1
        ac.last_message_at=now
        self.save_data(id)
    def on_voice_update(self,member,before,after):
        id=member.id
        if not self.exists(id):self.add(id,member.name)
        ac=self.accounts[id]
        now=self.get_now()
        ac.voice_count+=1
        ac.last_voice_joined=now
        self.save_data(id)
    def get_now(self):
        JST = timezone(timedelta(hours=+9), 'JST')
        return datetime.now(JST)

class Account:
    def __init__(self):
        self.id=0
        self.name=""
        self.last_mobile_active=None
        self.last_web_active=None
        self.last_desktop_active=None
        self.message_count=0
        self.last_message=""
        self.last_message_at=None
        self.voice_count=0
        self.last_voice_joined=None
    def to_data(self):
        return {
            "id":self.id,
            "name":self.name,
            "last_mobile_active":self.date2str(self.last_mobile_active),
            "last_web_active":self.date2str(self.last_web_active),
            "last_desktop_active":self.date2str(self.last_desktop_active),
            "message_count":self.message_count,
            "last_message":self.last_message,
            "last_message_at":self.date2str(self.last_message_at),
            "voice_count":self.voice_count,
            "last_voice_joined":self.date2str(self.last_voice_joined),
            }
    def date2str(self,time):
        time_format='%Y_%m_%d %H_%M_%S'
        if time is None:return "-"
        return time.strftime(time_format)
    def str2date(self,s):
        time_format='%Y_%m_%d %H_%M_%S'
        if s is None or s=="-":return None
        return datetime.strptime(s, time_format)
    def read(self,dic):
        self.id=dic["id"]
        self.name=dic["name"]
        self.last_mobile_active=self.str2date(dic["last_mobile_active"])
        self.last_web_active=self.str2date(dic["last_web_active"])
        self.last_desktop_active=self.str2date(dic["last_desktop_active"])
        self.message_count=dic["message_count"]
        self.last_message=dic["last_message"]
        self.last_message_at=self.str2date(dic["last_message_at"])
        self.voice_count=dic["voice_count"]
        self.last_voice_joined=self.str2date(dic["last_voice_joined"])