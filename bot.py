# bot.py
import asyncio
import datetime
import os
import typing

import discord
from discord import app_commands
from dotenv import load_dotenv

import pairings
import tournament

roundID = 1036666


# loads from dotenv
load_dotenv()
TOKEN = 'DISCORD_TOKEN'
GUILD_ID = 'GUILD_ID'

Pairings = pairings.PairingsManager()

client = discord.Client(intents=discord.Intents.all(),
                        status=discord.Status.idle,
                        activity=discord.Activity(type=discord.ActivityType.watching,
                                                  name="pairings  |  /help"))
tree = app_commands.CommandTree(client)
activeGuild = discord.Object(id=os.getenv(GUILD_ID))



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print("Loading commands...")
    await tree.sync(guild=activeGuild)
    print("Starting loop...")
    client.loop.create_task(blastHandler(5))
    print("Loaded!")
    print("---------------------------------------------------------")



@tree.command(name="help",
              description="Displays all commands for PairingsBot.",
              guild=discord.Object(id=os.getenv(GUILD_ID)))
async def pairingsHelp(interaction):
    commands = [("/help",                                    "Displays all commands for PairingsBot."),
                ("/configureblasts <school> <channel-id>",   "Sets the school to filter pairings by and the channel that blasts should be sent to."),
                ("/configuretournaments <tournament-id>",    "Sets the tournament to blast pairings from."),
                ("/pairings",                                "Posts the pairings from the most recent round for all teams."),
                ("/pairings <team-code>",                    "Post the pairings from the most recent round for a specific team."),
                ("/startblasts",                             "Start tournament blasts."),
                ("/stopblasts",                              "Stop tournament blasts.")]

    embed = discord.Embed(title="Commands",
                          timestamp=datetime.datetime.utcnow(),
                          color=0x4E2A84)
    embed.set_footer(text="PairingsBot made by Golf0ned")
    
    for i in range(len(commands)):
        embed.add_field(name=commands[i][0], value=commands[i][1], inline=False)

    await interaction.response.send_message(embed=embed)



@tree.command(name="configureblasts",
              description="Sets the school to filter pairings by and the channel that blasts should be sent to.",
              guild=activeGuild)
async def configureBlasts(interaction, school : str, channelid : str):
    if not isValidChannel(channelid):
        await interaction.response.send_message(f'{channelid} isn\'t a valid channel id. :smiling_face_with_tear:', ephemeral=True)
        return
    Pairings.setSchool(school)
    Pairings.setBlastChannel(channelid)
    await interaction.response.send_message(f'Sending blasts for **{school}** to {client.get_channel(int(channelid)).mention}. :sunglasses:', ephemeral=True)



@tree.command(name="configuretournament", description="Sets the tournament to blast pairings from.", guild=activeGuild)
async def configureTournament(interaction, tournamentid : str):
    if not Pairings.getBlastChannel():
        await interaction.response.send_message('Your blasts aren\'t configured---use `/configureblasts` first. :face_in_clouds:', ephemeral=True)
        return
    if not tournament.isValidTournament(tournamentid):
        await interaction.response.send_message(f'{tournamentid} isn\'t a valid tournament. :sweat:', ephemeral=True)
        return
    Pairings.initTournament(tournamentid)
    await interaction.response.send_message('Tournament configured! :trophy:', ephemeral=True)



@tree.command(name="pairings", description="Post the pairings from the most recent round (for a specific team, if specified).", guild=activeGuild)
async def pairings(interaction, team : typing.Optional[str]):
    await blast(team)



@tree.command(name="startblasts", description="Start tournament blasts.", guild=activeGuild)
async def startBlasts(interaction):
    if Pairings.isBlasting():
        await interaction.response.send_message('Blasts already started! :nerd:', ephemeral=True)
        return
    if not isValidChannel(Pairings.getBlastChannel()):
        await interaction.response.send_message('You haven\'t set a valid channel id. :sob:', ephemeral=True)
        return
    Pairings.startBlasting()
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name="pairings  |  /help"))
    await interaction.response.send_message('Started blasts. :loud_sound:', ephemeral=True)



@tree.command(name="stopblasts", description="Stop tournament blasts.", guild=activeGuild)
async def stopBlasts(interaction):
    if not Pairings.isBlasting():
        await interaction.response.send_message('Blasts are already off! :nerd:', ephemeral=True)
        return
    Pairings.stopBlasting()
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name="pairings  |  /help"))
    await interaction.response.send_message('Stopped blasts. :mute:', ephemeral=True)



async def blastHandler(interval):
    while(True):
        if Pairings.isBlasting() and Pairings.hasTournament():
            pairings.checkForRound()
            if Pairings.hasBlast():
                await blast(None)
        await asyncio.sleep(interval)

async def blast(team):
    if not pairings.isConfigured():
        await client.response.send_message('Tournament isn\'t configured---use `/configuretournament` first. :disappointed_relieved:', ephemeral=True)
        return
    
    roundInfo = pairings.getRoundInfo()
    if not roundInfo:
        await client.response.send_message('Round isn\'t out yet. :yawning_face:', ephemeral=True)
        return
    
    school = Pairings.getSchool()
    roundNum = Pairings.getCurRound()
    roundURL = tournament.getRoundURL(Pairings.getTournamentID(), roundNum)
    roundTeams = roundInfo[0]
    roundSides = roundInfo[1]
    roundOpponents = roundInfo[2]
    roundJudges = roundInfo[3]
    roundRooms = roundInfo[4]

    embed = discord.Embed(title="", url=roundURL, timestamp=datetime.datetime.utcnow(), color=0x4E2A84)
    
    # All pairings
    if not team:
        embed.title = f'All Pairings (Round {roundNum})'
        for i in range(len(roundTeams)):
            val = f'{roundSides[i]} vs. {roundOpponents[i]} | {roundJudges[i]} | {roundRooms[i]}'
            embed.add_field(name=f'{Pairings.getSchool()} {roundTeams[i]}', value=val, inline=False)

    # Specific team code
    else:
        index = validTeamCode(team, roundTeams)
        if not index:
            await client.response.send_message(f'{team} isn\'t a valid team code :pensive:', ephemeral=True)

        embed.title = f'Pairing for {school} {team.upper()} (Round {roundNum})'
        val = f'{roundJudges[index]} | {roundRooms[index]}'
        embed.add_field(name=f'{roundSides[index]} vs. {roundOpponents[index]}', value=val, inline=False)

    embed.set_footer(text="Good luck!")
    await client.response.send_message(embed=embed)



def isValidChannel(id : str):
    try:
        if not (client.get_channel(int(id))): raise Exception()
    except:
        return False
    return True



def validTeamCode(team, teams):
    try:
        index = teams.index(team.upper())
    except:
        try:    
            index = teams.index(reverseCode(team).upper())
        except:
            return False
    return index

def reverseCode(teamCode):
    # TODO: error for teams of 3
    return teamCode[::-1] if len(teamCode) == 2 else teamCode[2:4] + teamCode[0:2]



client.run(os.getenv(TOKEN))