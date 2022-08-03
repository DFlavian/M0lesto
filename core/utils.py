from .messages import *
from .service import *
from .team import *
import random 
import requests
from os.path import exists

emojis = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫"]

class util():
    def __init__(self):
        self.service1 = service("TestService", 8090)
        self.gamedata = "http://10.10.0.1/api/game.json"
        self.status = "http://10.10.0.1/api/reports/status.json"
        self.teamid = 7
        self.teamList = []
        self.serviceList = []
        self.debug = False
        self.bloodcount = 0
        self.emoji_to_role = {}

    def attacks(self, tick): return "http://10.10.0.1/api/reports/public/"+str(tick)+"/teamServices.json"
    
    def health(self, tick): return "http://10.10.0.1/api/reports/public/"+str(tick)+"/checks.json"
    
    async def print_all(channel, serviceList, teamList):
        await service_down(channel, random.choice(serviceList))
        await service_up(channel, random.choice(serviceList))
        await first_blood(channel, random.choice(serviceList), random.choice(teamList))
        await under_attack(channel, random.choice(serviceList), random.choice(teamList))
        await exploit_down(channel, random.choice(serviceList), "exploit1")
        await exploit_up(channel, random.choice(serviceList), "exploit1", 10)
        await service_patched(channel, random.choice(serviceList))
        
    def importServices(self):
        print("Importing services...")
        #TODO: Implement the importing
        serviceList = []
        '''
        serviceList.append(service("TestService", 8090))
        serviceList.append(service("PwnAAAAAA", 3434))
        serviceList.append(service("Webbe", 8080))'''
        d = self.get_data()
        c = 0
        for i in d["services"]:
            serviceList.append(service(i["name"], c))
            c += 1
        self.serviceList = serviceList
        return serviceList

    def importTeams(self):
        print("Importing teams...")
        teamList = []
        d = self.get_data()
        c = 0
        for i in d["teams"]:
            teamList.append(team(i["name"], c, len(self.serviceList)))
            c += 1
        self.teamList = teamList
        return teamList

    def get_data(self, data="gamedata", tick=0):
        if data == "gamedata":
            print("Getting data from game...")
            if self.debug == True:
                return json.loads(open("./testdata/game.json").read())
            r = requests.get(self.gamedata)
            return r.json()
        if data == "health":
            print("Getting data from services health...")
            if self.debug == True:
                return json.loads(open("./testdata/checks.json").read())
            r = requests.get(self.health(tick))
            #print response status
            print(r.status_code)
            print(self.health(tick))
            return r.json()
        if data == "attacks":
            print("Getting data from attacks...")
            if self.debug == True:
                return json.loads(open("./testdata/teamServices.json").read())
            r = requests.get(self.attacks(tick))
            print(self.attacks(tick))
            print(r.status_code)
            print(r.json())
            return r.json()
        if data == "status":
            print("Getting data from status...")
            if self.debug == True:
                if(exists("./testdata/status.json")):
                    return json.loads(open("./testdata/status.json").read())
                else:
                    return -1
            try:
                r = requests.get(self.status)
            except:
                pass
            return r.json()

    async def checks(self, channel, tick):
        print("Checks...")
        self.channel = channel
        self.tick = tick
        await self.check_services(self.channel, self.tick)
        await self.check_attacks(self.channel, self.tick)
        await self.check_exploits(self.channel, self.tick)
        self.bloodcount =  await self.check_blood(self.channel, self.bloodcount)

    def get_tick(self):
        d = self.get_data("status")
        return d["currentRound"]

    async def create_roles(self, guild, channel):
        print("Creating roles...")
        channel.send("Creating roles...")
        self.serviceList = self.importServices()
        self.teamList = self.importTeams()
        embed=disnake.Embed(title="Service role", description="Pick up your service role.", color=0x07e319)
        roles = {}
        for role in guild.roles:
            roles[role.name] = role

        for s in self.serviceList:
            if s.name in roles:
                print("skip")
                r = roles[s.name]
            else:
                r = await guild.create_role(name=s.name)
                print("adding " + s.name)
            em = emojis[len(self.emoji_to_role)]
            self.emoji_to_role[disnake.PartialEmoji(name=em)] = r.id
            s.role = r
            embed.add_field(name=s.name, value=em, inline=False)
        
        msg = await channel.send(embed=embed)
        print(msg.id)

        for i in range(len(self.emoji_to_role)):
            em = emojis[i]
            print("adding reaction " + em)
            await msg.add_reaction(em)

        self.channel = channel
        self.role_message_id = msg.id
        print(self.emoji_to_role)
        return self.emoji_to_role, self.role_message_id

    def check_start(self):
        if(self.get_data("status") == -1):
            print("Game not started")
            return False
        return True

    async def check_services(self, channel, tick):
        print("Checking services status...")
        d = self.get_data("health" ,tick)
        slist = [0]*len(self.serviceList)
        
        for i in d:
            if(i["teamId"] == self.teamid):
                print(i["exitCode"])
                msg = i["stdout"]
                serviceId = i["serviceId"]
                service = self.serviceList[serviceId]
                if(i["exitCode"] != 101 ):
                    if(service.status == "UP"):
                        print("Service down!")
                        self.serviceList[serviceId].status = "DOWM"
                        await service_down(channel, service, msg)
                    slist[serviceId] = 1
        c = 0
        for i in slist:
            print(i)
            if i == 0 and self.serviceList[c].status == "DOWM":
                print("Service up!")
                self.serviceList[c].status = "UP"
                await service_up(channel, self.serviceList[c])
            c += 1

    async def check_attacks(self, channel, tick):
        #TODO: Implement the function
        print("Checking attacks...")
        oldTeam = self.teamList[self.teamid]
        d = self.get_data("attacks", tick)
        for t in d:
            if(t["teamId"] == self.teamid):
                print(t["serviceId"])
                service = self.serviceList[t["serviceId"]]
                if service.status == "UP":
                    oldlost = oldTeam.services[t["serviceId"]]["lost"][0]
                    lost = t["lost"]
                    if lost > oldlost:
                        print("Service under attack!")
                        self.serviceList[t["serviceId"]].underattack = True
                        self.teamList[self.teamid].services[t["serviceId"]]["lost"][0] = lost
                        if self.teamList[self.teamid].services[t["serviceId"]]["lost"][1] == 0:
                            await under_attack(channel, service)
                        self.teamList[self.teamid].services[t["serviceId"]]["lost"][1] = -1
                    elif service.underattack == True:
                        if(self.teamList[self.teamid].services[t["serviceId"]]["lost"][1] == -1):
                            self.teamList[self.teamid].services[t["serviceId"]]["lost"][1] += 1
                        self.teamList[self.teamid].services[t["serviceId"]]["lost"][1] += 1
                        print("Lost: " + str(self.teamList[self.teamid].services[t["serviceId"]]["lost"][1]))

                    if self.teamList[self.teamid].services[t["serviceId"]]["lost"][1] > 3:
                        self.teamList[self.teamid].services[t["serviceId"]]["lost"][1] = 0
                        self.serviceList[t["serviceId"]].underattack = False
                        await service_patched(channel, service)
        return

    async def check_exploits(self, channel, tick):
        #TODO: Implement the function
        print("Checking the exploits...")
        oldteam = self.teamList[self.teamid]
        d = self.get_data("attacks", tick)
        for t in d:
            if(t["teamId"] == self.teamid):
                service = self.serviceList[t["serviceId"]]
                stolen = t["stolen"]
                oldstolen = oldteam.services[t["serviceId"]]["stolen"][0]
                if stolen > oldstolen:
                    print("We're exploiting!")
                    self.serviceList[t["serviceId"]].exploited = True
                    self.teamList[self.teamid].services[t["serviceId"]]["stolen"][0] = stolen
                    if self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1] == 0:
                        await exploit_up(channel, service)
                    self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1] = -1
                elif service.exploited == True:
                    if(self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1] == -1):
                        self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1] += 1
                    self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1] += 1
                    print("Stolen: " + str(self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1]))
                if self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1] > 3:
                    self.teamList[self.teamid].services[t["serviceId"]]["stolen"][1] = 0
                    self.serviceList[t["serviceId"]].exploited = False
                    await exploit_down(channel, service)
        return

    async def check_blood(self, channel, bloodcount):
        d = self.get_data("status")
        print(d)
        if(self.debug == True):
            return
        while(len(d["firstBloods"]) > bloodcount):
            print("First blood!")
            for b in d["firstBloods"]:
                sid = b["service_id"]
                tid = b["attacker_id"]
                if self.serviceList[sid].firstblood == False:
                    team = self.teamList[tid]
                    service = self.serviceList[sid]
                    self.serviceList[sid].firstblood = True
                    bloodcount += 1
                    await first_blood(channel, service, team)
        return bloodcount
