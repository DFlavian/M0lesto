
class Plugin:
    def __init__(self, *args, **kwargs):
        #print("Plugin initialized with args: " + str(args))
        both = args[0] # bot handler
        print(both.channel)

    
    async def run(self, *args, **kwargs):
        jbz_list = ["jbz", "z3r0n37", "flavian", "goten"]
        #print("Plugin run with args: " + str(args))
        msg = args[1]
        print(msg)
        if any(a in msg.content.lower() for a in jbz_list):
            print("jbz found")
            await msg.reply("lol jbz")
        if "AAAA" in msg.content:
            print("AAAAAAAAA found")
            await msg.reply("segmentation fault (core dumped)")