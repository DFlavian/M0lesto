
class Plugin:
    def __init__(self, *args, **kwargs):
        #print("Plugin initialized with args: " + str(args))
        both = args[0] # bot handler
        print(both.channel)

    
    async def run(self, *args, **kwargs):
        #print("Plugin run with args: " + str(args))
        msg = args[1]
        print(msg)