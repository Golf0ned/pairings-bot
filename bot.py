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
    commands = [("/help",                                             "Displays all commands for PairingsBot."),
                ("/configure <tournament-url>",  "Sets the tournament to blast pairings from and the event in the current channel."),
                ("/pairings",                                         "Posts the pairings from the most recent round for all teams."),
                ("/pairings <team-code>",                             "Post the pairings from the most recent round for a specific team."),
                ("/startblasts",                                      "Start tournament blasts."),
                ("/stopblasts",                                       "Stop tournament blasts.")]

    embed = discord.Embed(title="Commands",
                          timestamp=datetime.datetime.utcnow(),
                          color=0x4E2A84)
    embed.set_footer(text="PairingsBot made by Golf0ned")
    
    for i in range(len(commands)):
        embed.add_field(name=commands[i][0], value=commands[i][1], inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)



@tree.command(name="configureblasts",
              description="Sets the school to filter pairings by and the channel that blasts should be sent to.",
              guild=activeGuild)
async def configureBlasts(interaction, school : str, channel : discord.TextChannel):
    channelid = channel.id
    if not isValidChannel(channelid):
        await interaction.response.send_message(f'{channel} isn\'t a valid channel. :smiling_face_with_tear:', ephemeral=True)
        return
    Pairings.setSchool(school)
    Pairings.setBlastChannel(channelid)
    if Pairings.hasTournament():
        await interaction.response.send_message(f'Sending blasts for **{school}** to {client.get_channel(int(channelid)).mention}. :sunglasses:\nRemember to reconfigure the tournament!', ephemeral=True)
    else:
        await interaction.response.send_message(f'Sending blasts for **{school}** to {client.get_channel(int(channelid)).mention}. :sunglasses:', ephemeral=True)



@tree.command(name="configuretournament", description="Sets the tournament and event to blast pairings from.", guild=activeGuild)
async def configureTournament(interaction, tournamentid : str, eventid : str):
    if not Pairings.getBlastChannel():
        await interaction.response.send_message('Your blasts aren\'t configured---use `/configureblasts` first. :face_in_clouds:', ephemeral=True)
        return
    if not tournament.isValidTournament(tournamentid):
        await interaction.response.send_message(f'{tournamentid} isn\'t a valid tournament id. :sweat:', ephemeral=True)
        return
    if not tournament.isValidEvent(tournamentid, eventid):
        await interaction.response.send_message(f'{eventid} isn\'t a valid event id. :anguished:', ephemeral=True)
        return
    Pairings.initTournament(tournamentid, eventid)
    await interaction.response.send_message(f'Tournament configured! :trophy:\n(Tournament ID: **{tournamentid}**, Event ID: **{eventid}**)\n', ephemeral=True)



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
        await interaction.response.send_message('You haven\'t set a valid channel id. :sob:', ephemeral=True)
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
        await interaction.response.send_message('Tournament isn\'t configured---use `/configuretournament` first. :disappointed_relieved:', ephemeral=True)
        return
    
    roundInfo = Pairings.getRoundInfo()
    print(roundInfo)
    if interaction and not roundInfo:
        await interaction.response.send_message('Round isn\'t out yet. :yawning_face:', ephemeral=True)
        return
    
    school = Pairings.getSchool()
    roundNum = Pairings.getRoundNumber()
    roundURL = Pairings.getRoundURL()
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
            # basic team info
            val = f'{roundSides[i]} vs. [{roundOpponents[i][0]}]({roundOpponents[i][1]})\nJudge(s): '
            # add each judge
            for judge, paradigm in roundJudges[i]:
                val += f'[{judge}]({paradigm}), '
            # remove awkward final comma
            val = val[:-2]
            # add room
            val += f'\nRoom: {roundRooms[i]}'
            # add to embed
            embed.add_field(name=f'{Pairings.getSchool()} {roundTeams[i]}', value=val, inline=False)

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
