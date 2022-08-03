import pymongo
import json

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

def dropAll():
    servicecol = myclient["discordbot"]["services"]
    exploitcol = myclient["discordbot"]["exploit"]
    rolecol = myclient["discordbot"]["roles"]
    servicecol.drop()
    exploitcol.drop()
    rolecol.drop()

def insertService(s):
    servicecol = myclient["discordbot"]["services"]
    if servicecol.count_documents({"name": s.name}) == 0:
        #print(type(s.json()))
        return servicecol.insert_one(json.loads(s.json()))

def listServices():
    servicecol = myclient["discordbot"]["services"]
    x = servicecol.find()
    ris = []
    for i in x:
        print(i)
        ris.append(i)
    return ris

def updateService(s, rid):
    servicecol = myclient["discordbot"]["services"]
    listServices()
    servicecol.update_one({"name": s.name}, {"$set": {"role":rid}})

def insertTeam(t):
    teamcol = myclient["discordbot"]["teams"]
    if teamcol.count_documents({"name": t.name}) == 0:
        return teamcol.insert_one(json.loads(t.json()))

def listTeams():
    teamcol = myclient["discordbot"]["teams"]
    x = teamcol.find()
    ris = []
    for i in x:
        print(i)
        ris.append(i)
    return ris

def findTeamName(id):
    teamcol = myclient["discordbot"]["teams"]
    x = teamcol.find_one({"id": id})
    return x["name"]

def insertExploit(s):
    exploitcol = myclient["discordbot"]["exploit"]
    if exploitcol.count_documents({"name": s.name}) == 0:
        #print(type(s.json()))
        return exploitcol.insert_one(json.loads(s.json()))

def listExploits():
    exploitcol = myclient["discordbot"]["exploits"]
    x = exploitcol.find()
    ris = []
    for i in x:
        print(i)
        ris.append(i)
    return ris

def insertRole(guildid, roleid, name):
    rolecol = myclient["discordbot"]["roles"]
    if rolecol.count_documents({"guildid": guildid, "roleid": roleid}) == 0:
        return rolecol.insert_one({"guildid": guildid, "roleid": roleid, "name": name})

def listRole():
    rolecol = myclient["discordbot"]["roles"]
    x = rolecol.find()
    ris = []
    for i in x:
        print(i)
        ris.append(i)
    return ris

listServices()
listExploits()
listRole()
listTeams()
