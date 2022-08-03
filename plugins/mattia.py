
class Plugin:
    def __init__(self, *args, **kwargs):
        #print("Plugin initialized with args: " + str(args))
        both = args[0] # bot handler
        print(both.channel)

    
    async def run(self, *args, **kwargs):
        mattia_list = ["mattia", "brandon", "russi", "gta", "malware", "nitro", "sansa", "hetzner", "352791268289413130", "mc", "bangla", "referral"]
        #print("Plugin run with args: " + str(args))
        msg = args[1]
        print(msg)
        if any(a in msg.content.lower() for a in mattia_list):
            await msg.reply("Chi ha pwnato <@352791268289413130> ?")