from disnake.ext import commands
import disnake
from .service import *

GREEN = 0x07e319
RED = 0xff1100
YELLOW = 0xb0bd06

allowed_mentions = disnake.AllowedMentions.all()

async def service_down(channel, service, msg):
    embed=disnake.Embed(title="SERVICE DOWN!", description="**"+service.name+"** is down! **"+msg+"**", color=RED)
    await channel.send(service.role.mention,embed=embed, allowed_mentions = allowed_mentions)

async def service_up(channel, service):
    embed=disnake.Embed(title="SERVICE UP!", description="**"+service.name+"** is up again!", color=GREEN)
    await channel.send(embed=embed, allowed_mentions = allowed_mentions)

async def first_blood(channel, service, team):
    embed=disnake.Embed(title="FIRST BLOOD!", description="**"+team.name + "** first blooded **"+service.name+"**!", color=YELLOW)
    await channel.send(service.role.mention, embed=embed, allowed_mentions = allowed_mentions)

async def under_attack(channel, service):
    embed=disnake.Embed(title="UNDER ATTACK!",description="Someone is exploiting **"+service.name+"**!", color=RED)
    await channel.send(service.role.mention,embed=embed, allowed_mentions = allowed_mentions)

async def service_patched(channel, service):
    embed=disnake.Embed(title="SERVICE PATCHED!",description="We patched **"+service.name+"**!", color=GREEN)
    await channel.send(embed=embed, allowed_mentions = allowed_mentions)

async def exploit_down(channel, service):
    embed=disnake.Embed(title="EXPLOIT DOWN!",description="The exploit for the service **"+service.name+"** stopped working!", color=RED)
    await channel.send(service.role.mention,embed=embed, allowed_mentions = allowed_mentions)

async def exploit_up(channel, service):
    embed=disnake.Embed(title="WE'RE EXPLOITING!",description="We're exploiting **"+service.name+"**!", color=GREEN)
    await channel.send(embed=embed, allowed_mentions = allowed_mentions)