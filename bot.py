# bot.py
import os
import typing

import discord
from discord import app_commands
from dotenv import load_dotenv

validRounds = ["1", "2", "3", "4", "5", "6", "7", "8", "triples", "doubles", "octos", "quarters", "semis", "finals"]

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



@tree.command(name="help", description="Displays all commands for PairingsBot.", guild=discord.Object(id=os.getenv(GUILD_ID)))
async def pairingsHelp(interaction):
    
    commands = ["/help",
                "/configureblasts <channel-id>",
                "/configuretournaments <school> <tournament-id>",
                "/pairings",
                "/pairings <team-code>"]
    
    descriptions = ["Displays all commands for PairingsBot.",
                    "Sets the channel that blasts should be sent to.",
                    "Sets the school to filter pairings by and the tournament to look at.",
                    "Posts the pairings from the most recent round for all teams.",
                    "Post the pairings from the most recent round for a specific team."]

    embed = discord.Embed(title="Commands",
                          color=0x4E2A84)
    for i in range(len(commands)):
        embed.add_field(name=commands[i], value=descriptions[i], inline=False)
    embed.set_footer(text="Made by Golf0ned")

    await interaction.response.send_message(embed=embed)



@tree.command(name="pairings", description="Post the pairings from the most recent round (for a specific team, if specified).", guild=discord.Object(id=os.getenv(GUILD_ID)))
async def pairings(interaction, team : typing.Optional[str]):
    roundNum = 6
    tournID = 28074
    roundID = 1036666
    school = "Northwestern"
    teams = ["DC", "LA"]
    sides = ["Aff", "Neg"]
    opponents = ["UC Berkeley FT", "Michigan DW"]
    judges = ["Lee Quinn", "Nate Milton"]
    rooms = ["GRN 251/BR24", "TRB C115/BR66"]

    if not team:
        embed = discord.Embed(title=f'Pairings (Round {roundNum})',
                            url=f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournID}&round_id={roundID}',
                            color=0x4E2A84)
        for i in range(2):
            val = f'{sides[i]} vs. {opponents[i]} | {judges[i]} | {rooms[i]}'
            embed.add_field(name=f'{school} {teams[i]}', value=val, inline=False)
        embed.set_footer(text="Good luck!")

    else:
        embed = discord.Embed(title=f'Pairing for {school} {team} (Round {roundNum})',
                            url=f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournID}&round_id={roundID}',
                            color=0x4E2A84)
        try:
            index = teams.index(team)
        except:
            try:    
                index = teams.index(reverseCode(team))
            except:
                await interaction.response.send_message("That wasn't a valid team code :pensive:", ephemeral=True)
                return
        val = f'{sides[index]} vs. {opponents[index]} | {judges[index]} | {rooms[index]}'
        embed.add_field(name=f'{school} {team}', value=val, inline=False)
        embed.set_footer(text="Good luck!")

    await interaction.response.send_message(embed=embed)

# @tree.command(name="configure", guild=discord.Object(id=os.getenv(GUILD_ID)))
# async def configureTournament(interaction, pairingsURL):
def reverseCode(teamCode):
    # TODO: error for teams of 3
    return teamCode[::-1] if len(teamCode) == 2 else teamCode[2:4] + teamCode[0:2]

client.run(os.getenv(TOKEN))