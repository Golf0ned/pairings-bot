# bot.py
import os
import discord
from discord import app_commands
from dotenv import load_dotenv

# loads from dotenv
load_dotenv()
TOKEN = 'DISCORD_TOKEN'
GUILD_ID = 'GUILD_ID'

intents = discord.Intents.all()
client = discord.Client(intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="pairings"))
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print("Loading commands...")
    await tree.sync(guild=discord.Object(id=os.getenv(GUILD_ID)))
    print("Loaded!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'test' in message.content:
        await message.channel.send('test :)')

@tree.command(name="help", description="Displays all commands for PairingsBot.", guild=discord.Object(id=os.getenv(GUILD_ID)))
async def pairingsHelp(interaction):
    commands = ["help", "getpairings"]
    descriptions = ["Displays all commands for PairingsBot.", "Gets Pairings."]

    embed = discord.Embed(title="Commands",
                          color=0x4E2A84)
    embed.set_footer(text="Made by Golf0ned")
    for i in range(2):
        embed.add_field(name=commands[i], value=descriptions[i], inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="getpairings", description="Gets pairings.", guild=discord.Object(id=os.getenv(GUILD_ID)))
async def getPairings(interaction):
    roundNum = 6
    tournID = 28074
    roundID = 1036666

    teams = ["Northwestern DC", "Northwestern LA"]
    sides = ["Aff", "Neg"]
    opponents = ["UC Berkeley FT", "Michigan DW"]
    judges = ["Lee Quinn", "Nate Milton"]
    rooms = ["GRN 251/BR24", "TRB C115/BR66"]


    embed = discord.Embed(title=f'Pairings (Round {roundNum})',
                          url=f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournID}&round_id={roundID}',
                          color=0x4E2A84)
    embed.set_footer(text="Good luck!")
    for i in range(2):
        val = f'{sides[i]} vs. {opponents[i]} | {judges[i]} | {rooms[i]}'
        embed.add_field(name=teams[i], value=val, inline=False)
    await interaction.response.send_message(embed=embed)

# @tree.command(name="configure", guild=discord.Object(id=os.getenv(GUILD_ID)))
# async def configureTournament(interaction, pairingsURL):


client.run(os.getenv(TOKEN))