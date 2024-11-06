from pymongo import MongoClient
import datetime
import requests
import json
from bs4 import BeautifulSoup
from config import mongo
cluster=MongoClient(mongo)
db=cluster["UsersData"]

vyatsu_db=db["vyatsu"]

def login():
    login=vyatsu_db.find_one({"type":"config"})["login"]
    password=vyatsu_db.find_one({"type":"config"})["password"]

    log=requests.post("https://new.vyatsu.ru/account/pers/?login=yes",headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36"},data={"AUTH_FORM": "Y","TYPE": "AUTH","backurl": "/account/pers/","USER_LOGIN": login,"USER_PASSWORD": password,"USER_REMEMBER": "Y","Login": "Войти"})
    if "выйти" in log.text.lower():
        vyatsu_db.update_one({"type":"session"},{"$set":{"session":str(log.cookies.get_dict())}})
        return "Login Success"
    else: return "Error"

def rasp_parse():
    cooks=vyatsu_db.find_one({"type":"session"})["session"].replace("\'","\"")
    rasp=requests.get("https://new.vyatsu.ru/account/obr/rasp/",cookies=json.loads(cooks),headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36"})
    if "выйти" in rasp.text.lower():
        raspp=BeautifulSoup(rasp.text,"lxml")
        rasp_text={}
        for i in raspp.find_all("div",class_="mx-auto p-5 md:px-0 day-container"):
            day=i.find("div",class_="px-5 md:px-16 py-7 text-lg font-normal").text.replace("\n","")
            rasp_text[day]=[]
            for i1 in i.find_all("div",class_="flex flex-col day-pair"):
                print(i1.text.split())
                rasp_text[day].append({"number":i1.text.split()[1],"time":i1.text.split()[2],"room":i1.text.split()[-1],"type":i1.text.split(",")[-3].strip(),"teacher":i1.text.split(",")[-2].strip(),"name":" ".join(i1.text.split()[3:]).split(",")[0].strip()})
    else:
        rasp_text={}
    return rasp_text

    


