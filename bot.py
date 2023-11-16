# bot.py
import os
import typing
import asyncio

import discord
from discord import app_commands
from dotenv import load_dotenv
import pairings



# loads from dotenv
load_dotenv()
TOKEN = 'DISCORD_TOKEN'
GUILD_ID = 'GUILD_ID'

activeChannel = 1059975075790589994
Pairings = pairings.PairingsManager()
Pairings.setSchool("Northwestern")
Pairings.setTournament(28074)
roundID = 1036666


intents = discord.Intents.all()
client = discord.Client(intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="pairings  |  /help"))
tree = app_commands.CommandTree(client)
activeGuild = discord.Object(id=os.getenv(GUILD_ID))



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print("Loading commands...")
    await tree.sync(guild=activeGuild)
    print("Starting loop...")
    client.loop.create_task(blast())
    print("Loaded!")



@tree.command(name="help",
              description="Displays all commands for PairingsBot.",
              guild=discord.Object(id=os.getenv(GUILD_ID)))
async def pairingsHelp(interaction):
    
    commands = ["/help",
                "/configureblasts <school> <channel-id>",
                "/configuretournaments <tournament-id>",
                "/pairings",
                "/pairings <team-code>",
                "/startblasts",
                "/stopblasts"]
    
    descriptions = ["Displays all commands for PairingsBot.",
                    "Sets the school to filter pairings by and the channel that blasts should be sent to.",
                    "Sets the tournament to blast pairings from.",
                    "Posts the pairings from the most recent round for all teams.",
                    "Post the pairings from the most recent round for a specific team.",
                    "Start tournament blasts.",
                    "Stop tournament blasts."]

    embed = discord.Embed(title="Commands",
                          color=0x4E2A84)
    for i in range(len(commands)):
        embed.add_field(name=commands[i], value=descriptions[i], inline=False)
    embed.set_footer(text="Made by Golf0ned")

    await interaction.response.send_message(embed=embed)



@tree.command(name="configureblasts",
              description="Sets the school to filter pairings by and the channel that blasts should be sent to.",
              guild=activeGuild)
async def configureBlasts(interaction, school : str, channelid : str):
    if not client.get_channel(int(Pairings.getBlastChannel())):
        await interaction.response.send_message(f'{channelid} isn\'t a valid channel id. :smiling_face_with_tear:', ephemeral=True)
        return
    Pairings.setSchool(school)
    Pairings.setBlastChannel(channelid)
    print(Pairings.getBlastChannel())
    await interaction.response.send_message('Channel and school configured! :sunglasses:', ephemeral=True)



@tree.command(name="configuretournament", description="Sets the tournament to blast pairings from.", guild=activeGuild)
async def configureTournament(interaction, pairingsurl : str):
    await interaction.response.send_message('Tournament configured! :trophy:', ephemeral=True)



@tree.command(name="pairings", description="Post the pairings from the most recent round (for a specific team, if specified).", guild=activeGuild)
async def pairings(interaction, team : typing.Optional[str]):
    roundNum = 6

    teams = ["DC", "LA"]
    sides = ["Aff", "Neg"]
    opponents = ["UC Berkeley FT", "Michigan DW"]
    judges = ["Lee Quinn", "Nate Milton"]
    rooms = ["GRN 251/BR24", "TRB C115/BR66"]

    # default value (all teams)
    if not team:
        embed = discord.Embed(title=f'Pairings (Round {roundNum})',
                            url=Pairings.getRoundURL(roundNum),
                            color=0x4E2A84)
        for i in range(2):
            val = f'{sides[i]} vs. {opponents[i]} | {judges[i]} | {rooms[i]}'
            embed.add_field(name=f'{Pairings.getSchool()} {teams[i]}', value=val, inline=False)
        embed.set_footer(text="Good luck!")

    # team code (specific team)
    else:
        embed = discord.Embed(title=f'Pairing for {Pairings.getSchool()} {team.upper()} (Round {roundNum})',
                            url=Pairings.getRoundURL(roundNum),
                            color=0x4E2A84)
        try:
            index = teams.index(team.upper())
        except:
            try:    
                index = teams.index(reverseCode(team).upper())
            except:
                await interaction.response.send_message(f'{team} isn\'t a valid team code :pensive:', ephemeral=True)
                return
        val = f'{sides[index]} vs. {opponents[index]} | {judges[index]} | {rooms[index]}'
        embed.add_field(name=f'{Pairings.getSchool()} {team}', value=val, inline=False)
        embed.set_footer(text="Good luck!")

    await interaction.response.send_message(embed=embed)



@tree.command(name="startblasts", description="Start tournament blasts.", guild=activeGuild)
async def startBlasts(interaction):
    if Pairings.isBlasting():
        await interaction.response.send_message('Blasts already started! :nerd:', ephemeral=True)
        return
    Pairings.startBlasting()
    await interaction.response.send_message('Started blasts. :mega:', ephemeral=True)



@tree.command(name="stopblasts", description="Stop tournament blasts.", guild=activeGuild)
async def stopBlasts(interaction):
    await interaction.response.send_message('Stopped blasts. :mute:', ephemeral=True)
    Pairings.stopBlasting()



async def blast():
    while(True):
        if Pairings.isBlasting():
            # TODO: actually blast stuff
            # TODO: error handling for invalid channel
            await client.get_channel(int(Pairings.getBlastChannel())).send('Test blast')
        await asyncio.sleep(5)



def reverseCode(teamCode):
    # TODO: error for teams of 3
    return teamCode[::-1] if len(teamCode) == 2 else teamCode[2:4] + teamCode[0:2]

client.run(os.getenv(TOKEN))