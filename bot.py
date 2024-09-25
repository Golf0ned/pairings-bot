import datetime
import os
import random

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from src import tabroom


#
# Load pile for dotenv/bot global variables.
#
load_dotenv()

# Discord
discord_token = os.getenv('DISCORD_TOKEN')
discord_guild_id = os.getenv('DISCORD_GUILD_ID')
discord_active_channel_id = None
discord_blasting = False

# School config
school_name = os.getenv('SCHOOL_NAME')
school_judges = os.getenv('SCHOOL_JUDGES').split(',')

# Tournament config
tournament_tourn_id = None
tournament_events_id = []
tournament_events_name = []
tournament_prev_data = []


#
# Bot setup proper.
#
bot = discord.Bot(intents=discord.Intents.all(),
                  status=discord.Status.idle,
                  activity=discord.Activity(type=discord.ActivityType.watching,
                                            name="pairings  |  /help",
                                            )
                  )

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Starting blast handler...')
    blast_handler.start()
    print('Ready!')
    print('------')


#
# Bot commands.
#
@bot.slash_command(name="configure",
                   description="Sets the tournament to blast pairings from in the current channel.",
                   guild_ids=[discord_guild_id])
async def configure(ctx, url: str):
    # url format: https://www.tabroom.com/index/tourn/index.mhtml?tourn_id=<TOURN_ID>
    split_url = url.split('=')
    if split_url[0] != 'https://www.tabroom.com/index/tourn/index.mhtml?tourn_id':
        await ctx.respond('Invalid URL format. Please provide a Tabroom invite URL.')
        return

    tourn_id = split_url[1] # Local, so invalid doesn't affect global
    if not tabroom.is_valid_tournament(tourn_id):
        await ctx.respond('Invalid tournament. Please check the URL and try again.')
        return
   
    global discord_active_channel_id, tournament_tourn_id, tournament_events_id, tournament_events_name, tournament_prev_data

    discord_active_channel_id = ctx.channel_id
    tournament_tourn_id = tourn_id
    (tournament_events_id, tournament_events_name) = tabroom.get_events(tourn_id)
    tournament_prev_data = [[] for _ in tournament_events_id]

    await ctx.respond(f'Tournament configured to send pairings in {ctx.channel.mention}! :trophy:\n(Tournament ID: {tournament_tourn_id})')


@bot.slash_command(name="startblasts",
                   description="Starts tournament blasts.",
                   guild_ids=[discord_guild_id])
async def start_blasts(ctx):
    global discord_blasting
    if discord_blasting:
        await ctx.respond('Blasts already started! :nerd:')
        return
    if not tournament_tourn_id:
        await ctx.respond('Tournament not configured. :sob:')
        return
    discord_blasting = True
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name="pairings  |  /help",
                                                        )
                              )
    await ctx.respond('Blasting started! :loud_sound:')


@bot.slash_command(name="stopblasts",
                   description="Stops tournament blasts.",
                   guild_ids=[discord_guild_id])
async def stop_blasts(ctx):
    global discord_blasting
    if not discord_blasting:
        await ctx.respond('Blasts already stopped! :nerd:')
        return
    discord_blasting = False
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name="pairings  |  /help",
                                                        )
                              )
    await ctx.respond('Blasting stopped! :mute:')


#
# Blast handler.
#
@tasks.loop(seconds=10)
async def blast_handler():
    if discord_blasting and tournament_prev_data:
        for i in range(len(tournament_prev_data)):
            new_data = tabroom.get_pairings(tournament_tourn_id, tournament_events_id[i])
            prev_data = tournament_prev_data[i]
            cur_data = tabroom.filter_round_data(new_data[1], new_data[0], school_name, school_judges)
            if cur_data[1] and tabroom.is_valid_blast(prev_data, cur_data):
                tournament_prev_data[i] = cur_data
                await blast_pairings(None, cur_data, tournament_events_name[i])


async def blast_pairings(ctx, data, event_name):
    if not data or not data[1]: return
    if ctx:
        if not tournament_tourn_id:
            await ctx.respond('No tournament configured. Please use /configure to set the tournament. :disappointed_relieved:')
            return
        if not data:
            await ctx.respond('No data to blast. :yawning_face:')
            return
    
    # print(f'{event_name}: {data}')

    # It's embed building o'clock.
    embed = discord.Embed(title=f'Pairings ({event_name}, Round {data[0][0]})',
                          color=0x4E2A84,
                          timestamp=datetime.datetime.now(),
                          )
    embed.set_footer(text=random_pairings_message())
    for pairing in data[1][0]:
        val = f'{pairing[1]} vs [{pairing[2][0]}]({pairing[2][1]})\nJudge(s): '
        for judge, paradigm in pairing[3]:
            val += f'[{judge}]({paradigm}), '
        val = val[:-2]
        val += f'\nRoom: {pairing[4]}'
        embed.add_field(name=f'{school_name} {pairing[0]}',
                        value=val,
                        inline=False,
                        )
    for pairing in data[1][1]:
        val = f'{pairing[2]} vs {pairing[3]}\nRoom: {pairing[4]}'
        embed.add_field(name=f'JUDGE {pairing[0]}',
                        value=val,
                        inline=False,
                        )

    # Send formatted embed.
    if ctx:
        await ctx.respond(embed=embed)
    else:
        channel = bot.get_channel(discord_active_channel_id)
        await channel.send(embed=embed)


#
# Random message at bottom of embeds. For fun.
#
def random_pairings_message():
    messages = ["Good luck!",
                "Remember to stay hydrated!",
                "Reminder to ingest caffeine!",
                "\"Prompt disclosure, please.\"",
                "Zoom zoom, go to room.",
                ]
    return messages[random.randrange(len(messages))]



#
# Client run lmao.
#
bot.run(discord_token)
