# bot.py
import datetime
import os
import random
import typing

import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

from src import pairings, tournament

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

SCHOOL = os.getenv('SCHOOL')
JUDGES = os.getenv('JUDGES').split(',')

DEBUG = int(os.getenv('DEBUG'))

Pairings = pairings.PairingsManager()

client = discord.Client(intents=discord.Intents.all(),
                        status=discord.Status.idle,
                        activity=discord.Activity(type=discord.ActivityType.watching,
                                                  name="pairings  |  /help"))
tree = app_commands.CommandTree(client)
activeGuild = discord.Object(id=GUILD_ID)



@client.event
async def on_ready():
    if DEBUG:
        print('[DEBUG] Debug is on.')
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print("Loading commands...")
    await tree.sync(guild=activeGuild)
    print("Starting blast handler...")
    blastHandler.start()
    print("Loaded!")
    print("---------------------------------------------------------")



@tree.command(name="help",
              description="Displays all commands for PairingsBot.",
              guild=activeGuild)
async def pairingsHelp(interaction):
    commands = [("/help",                       "Displays all commands for PairingsBot."),
                ("/configure <tournament-url>", "Sets the tournament to blast pairings from and the event in the current channel."),
                ("/pairings",                   "Posts the pairings from the most recent round for all teams."),
                ("/pairings <team-code>",       "Post the pairings from the most recent round for a specific team."),
                ("/startblasts",                "Start tournament blasts."),
                ("/stopblasts",                 "Stop tournament blasts.")]

    embed = discord.Embed(title="Commands",
                          timestamp=datetime.datetime.now(datetime.timezone.utc),
                          color=0x4E2A84)
    embed.set_footer(text="PairingsBot made by @Golf0ned")
    
    for i in range(len(commands)):
        embed.add_field(name=commands[i][0], value=commands[i][1], inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)



@tree.command(name="configure",
              description="Sets the tournament and event to blast pairings from in the current channel.",
              guild=activeGuild)
async def configure(interaction, url : str):
    # filter url first. a bit hacky but im tired
    try:
        split = url.replace('&', '=').split('=')
        tournID, eventID = split[1], split[3]
        if not tournament.isValidEvent(tournID, eventID): raise Exception()
    except:
        await interaction.response.send_message(f'Invalid URL ({url}). :sweat:', ephemeral=True)
        return

    # actual config stuff
    channelid = interaction.channel_id
    Pairings.setSchool(SCHOOL)
    Pairings.setJudges(JUDGES)
    Pairings.setBlastChannel(channelid)
    Pairings.initTournament(tournID, eventID)
    await interaction.response.send_message(f'Tournament configured! :trophy:\n(Tournament ID: **{tournID}**, Event ID: **{eventID}**)', ephemeral = True)



@tree.command(name="pairings", description="Post the pairings from the most recent round (for a specific team, if specified).", guild=activeGuild)
async def pairings(interaction, team : typing.Optional[str]):
    await blast(interaction, team)



@tree.command(name="startblasts", description="Start tournament blasts.", guild=activeGuild)
async def startBlasts(interaction):
    print("Starting blasts.")
    if Pairings.isBlasting():
        await interaction.response.send_message('Blasts already started! :nerd:', ephemeral=True)
        return
    if not isValidChannel(Pairings.getBlastChannel()):
        await interaction.response.send_message('Tournament not configured. :sob:', ephemeral=True)
        return
    Pairings.startBlasting()
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name="pairings  |  /help"))
    await interaction.response.send_message('Started blasts. :loud_sound:', ephemeral=True)



@tree.command(name="stopblasts", description="Stop tournament blasts.", guild=activeGuild)
async def stopBlasts(interaction):
    print("Stopping blasts.")
    if not Pairings.isBlasting():
        await interaction.response.send_message('Blasts are already off! :nerd:', ephemeral=True)
        return
    Pairings.stopBlasting()
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name="pairings  |  /help"))
    await interaction.response.send_message('Stopped blasts. :mute:', ephemeral=True)


@tasks.loop(seconds=8)
async def blastHandler():
    if Pairings.isBlasting() and Pairings.hasTournament():
        Pairings.checkForRound()
        if Pairings.hasBlast():
            print("Received blast!")
            await blast(None, None)

async def blast(interaction, team):
    if interaction and not Pairings.hasTournament():
        await interaction.response.send_message('Tournament isn\'t configured---use `/configure` first. :disappointed_relieved:', ephemeral=True)
        return
    
    roundInfo = Pairings.getRoundInfo()
    # print(roundInfo)
    if interaction and not roundInfo:
        await interaction.response.send_message('Round isn\'t out yet. :yawning_face:', ephemeral=True)
        return
    
    school = Pairings.getSchool()
    roundNum = Pairings.getRoundNumber()
    roundURL = Pairings.getRoundURL()

    debaterTeams = roundInfo[0][0]
    debaterSides = roundInfo[0][1]
    debaterOpponents = roundInfo[0][2]
    debaterJudges = roundInfo[0][3]
    debaterRooms = roundInfo[0][4]

    judgeNames = roundInfo[1][0]
    judgePanels = roundInfo[1][1]
    judgeTeam1 = roundInfo[1][2]
    judgeTeam2 = roundInfo[1][3]
    judgeRooms = roundInfo[1][4]

    embed = discord.Embed(title="", url=roundURL,
                          timestamp=datetime.datetime.now(datetime.timezone.utc),
                          color=0x4E2A84)
    
    # All pairings
    if not team:
        embed.title = f'All Pairings (Round {roundNum})'
        for i in range(len(debaterTeams)):
            # basic team info
            val = f'{debaterSides[i]} vs. [{debaterOpponents[i][0]}]({debaterOpponents[i][1]})\nJudge(s): '
            # add each judge
            for judge, paradigm in debaterJudges[i]:
                val += f'[{judge}]({paradigm}), '
            # remove awkward final comma
            val = val[:-2]
            # add room
            val += f'\nRoom: {debaterRooms[i]}'
            # add to embed
            embed.add_field(name=f'{Pairings.getSchool()} {debaterTeams[i]}', value=val, inline=False)
        for i in range(len(judgeNames)):
            # competitors
            val = f'{judgeTeam1[i]} vs. {judgeTeam2[i]}\n'
            # rest of panel, if existent
            if len(judgePanels[i]) != 1:
                val += f'Panel: {", ".join(judge for judge in judgePanels[i])}\n'
            # room
            val += f'Room: {judgeRooms[i]}'
            # add to embed
            embed.add_field(name=f'[Judge] {judgeNames[i]}', value=val, inline=False)

    # Specific team code
    else:
        index = validTeamCode(team, roundTeams)
        if interaction and index < 0:
            await interaction.response.send_message(f'{team} isn\'t a valid team code :pensive:', ephemeral=True)
            return

        embed.title = f'Pairing for {school} {team.upper()} (Round {roundNum})'
        val = f'Judge(s): {roundJudges[index]}\nRoom: {roundRooms[index]}'
        embed.add_field(name=f'{roundSides[index]} vs. {roundOpponents[index]}', value=val, inline=False)
    
    embed.set_footer(text=randomPairingsMessage())
    
    if interaction:
        await interaction.response.send_message(embed=embed)
    else:
        channel = client.get_channel(int(Pairings.getBlastChannel()))
        await channel.send(f'@everyone Pairings are out for round {roundNum}!')
        await channel.send(embed=embed)



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
            return -1
    return index

def reverseCode(teamCode):
    # TODO: error for teams of 3
    return teamCode[::-1] if len(teamCode) == 2 else teamCode[2:4] + teamCode[0:2]



def randomPairingsMessage():
    messages = [
                "Good luck!",
                "Remember to stay hydrated!",
                "Reminder to ingest caffeine!",
                "\"Prompt disclosure, please.\"",
                "Zoom zoom, go to room."
                ]
    return messages[random.randrange(len(messages))]



if DEBUG:
    @tree.command(name="quickconfig", description="Quick config for testing.", guild=activeGuild)
    async def quickConfig(interaction):
        school = 'Northwestern'
        channelid = '1175658371257475163'
        tournamentid = '29623'
        eventid = '273562'

        Pairings.setSchool(school)
        Pairings.setBlastChannel(channelid)
        Pairings.initTournament(tournamentid, eventid)
        await interaction.response.send_message('[DEBUG] Quick configured!', ephemeral=True)
        print(f'school: {school}\nchannelid: {channelid}\ntournamentid: {tournamentid}\neventid: {eventid}\n')

    @tree.command(name="testblast", description="Test for blast received.", guild=activeGuild)
    async def testBlast(interaction):
        Pairings.testBlast()
        await interaction.response.send_message('[DEBUG] Testing blast.', ephemeral=True)


client.run(TOKEN)
