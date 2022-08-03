import random

class Plugin:
    def __init__(self, *args, **kwargs):
        #print("Plugin initialized with args: " + str(args))
        both = args[0] # bot handler
        print(both.channel)

    
    async def run(self, *args, **kwargs):
        mattia_list = ["molesto", "m0lesto", "984403749701287956"]
        #print("Plugin run with args: " + str(args))
        msg = args[1]
        print(msg)
        if any(a in msg.content.lower() for a in mattia_list):
            for _ in range(random.randint(1,6)):
                await msg.reply("Mi hai chiamato?")

