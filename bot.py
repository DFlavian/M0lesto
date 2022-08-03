#!/usr/bin/env python3

import os
from disnake.ext import commands, tasks
import disnake
from dotenv import load_dotenv
from sqlalchemy import null
from core.messages import *
from core.service import *
from core.utils import *
from core.team import *
from datetime import datetime
from importlib import import_module

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

description = "POLITO bot for A&D"

class MyClient(disnake.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.tick = 0 
        self.util = util()
        

        # start the task to run in the background
        self.game_start.start() # start the task

        self.guild_id = os.getenv('SERVER_ID') #The ID of the server
        self.channel = 0 #The channel where the bot will post the messages
        self.gamestarted = False #True if the game has started
        self.timestampstart = 1656579600 #The timestamp of the game start
        self.setupflag = False

        self.role_message_id = 0  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {} # Dictionary that maps an emoji to a role.
        self.plugins = []
        self.import_plugins()


    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    #Create the roles
    async def setup(self):
        """Sets up the bot."""
        # Create a role for the bot to use.
        self.emoji_to_role, self.role_message_id = await self.util.create_roles( self.guild, self.channel)
        print(self.emoji_to_role)

    @commands.slash_command(name="idk", description="This is a test command")
    async def idk(ctx):
        await ctx.send("test")
        pass


    async def on_message(self, message):
        #Check if it's the bot
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!test"):
            await util.print_all(message.channel, self.serviceList, self.teamList)

        if message.content.startswith("!setup"):
            await message.channel.send(f"Waiting for the game to start...")
            self.channel = message.channel
            self.guild = message.guild
            self.guild_id = self.guild.id
            self.setupflag = True
            print(self.channel)
            
        
        if message.content.startswith("!start"):
            print("Starting game...")
        
        if message.content.startswith("!time"):
            #split message
            split = message.content.split(" ")
            time = split[1]
            print(time)

        await self.run_plugins(message) # Run all the modules
                

    @tasks.loop(seconds=5)
    async def game_start(self):
        if(self.gamestarted == False and self.setupflag == True):
            startgamedate = datetime.fromtimestamp(self.timestampstart)
            timestamp = datetime.timestamp(datetime.now())

            currenttime = datetime.fromtimestamp(timestamp)

            print(startgamedate)

            while(timestamp < self.timestampstart):
                timestamp = datetime.timestamp(datetime.now())
                return
            print("Time OK")
            while(not self.util.check_start()):
                return
            self.gamestarted = True
            if(self.channel != 0):
                await self.channel.send(f"@everyone Game started at {currenttime}")
            print("Game started!")
            await self.setup()
            self.tick_task.start()
            self.game_start.stop()
    
    @game_start.before_loop
    async def before_game_start(self):
        await self.wait_until_ready()

    @tasks.loop(seconds=120)  # task runs every 60 seconds
    async def tick_task(self):
        if(self.channel != 0):
            self.tick = self.util.get_tick()
            print(f"Tick: {self.tick}")
            print("Tick: " + str(self.tick))
            await self.util.checks(self.channel, self.tick)

    @tick_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in
        if(self.channel == 0):
            return
        print(self.channel.id)
        channel = self.channel  # channel ID goes here
        if not isinstance(channel, disnake.TextChannel):
            raise ValueError("Invalid channel")

        self.channel = channel
    
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        print("Reactiooon")
        if payload.guild_id is None or payload.member is None:
            print("idk")
            return

        if payload.user_id == self.user.id:
            return

        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            print(f"Messageid: {payload.message_id}")
            print(f"role_message_id: {self.role_message_id}")
            print("Message error")
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            print("Problem with guild")
            return

        try:
            print(payload.emoji)
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            print("Error roleid")
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            print("Role not valid")
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except disnake.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: disnake.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        if payload.guild_id is None:
            return
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except disnake.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
    
    # Import all the plugins
    def import_plugins(self):
        for file in os.listdir("./plugins"):
            if file.endswith(".py"):
                moduleh = import_module("plugins." + file[:-3]) # Import the module handler
                self.plugins.append(moduleh.Plugin(self))
    
    async def run_plugins(self, *args):
        for plugin in self.plugins:
            print(plugin)
            await plugin.run(self, *args)



intents = disnake.Intents.all()
intents.members = True

client = MyClient(intents=intents)
client.run(TOKEN)

