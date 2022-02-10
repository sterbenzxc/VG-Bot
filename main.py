import os
import discord
import requests
import json
import datetime
import pytz
import math
import DiscordUtils
from discord.ext import commands

client = commands.Bot(command_prefix='/')

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

@client.event
async def on_ready():
    print('Started')

@client.command()
async def pega(ctx, arg):
    response_g = requests.get("https://api-apollo.pegaxy.io/v1/game-api/pega/" + arg)
    json_data_g = json.loads(response_g.text)
    response = requests.get("https://api-apollo.pegaxy.io/v1/pegas/" + arg)
    json_data = json.loads(response.text)
    embed=discord.Embed(
    title="#"+ arg +"  **" + str(json_data['name'])+"**",
        url="",
        description="",
        color=discord.Color.blue())
    embed.set_thumbnail(url=str(json_data_g['pega']['design']['avatar_2']))
    embed.add_field(name=str(json_data['bloodLine']) + " • " + str(json_data['breedType']) + " • " + str(json_data['gender']), value="*Energy*: `" + str(json_data['energy']) + "/25`", inline=False)
    embed.add_field(name="**Breed Count**", value=str(json_data['breedCount']) + "/7", inline=False)
    embed.add_field(name="**Career**", value="*Total Win*: " + str(json_data['win']) + "\n *Total Lose*: " + str(json_data['lose']) + "\n *Total Races*: " + str(json_data['pegaTotalRaces'])+ "\n *Win Rate*: " + str(json_data['winRate'] * 100) + "%", inline=False)
    embed.add_field(name="**Parents**", value="*Father ID*: " + str(json_data['fatherId']) + "\n *Mother ID*: " + str(json_data['motherId']), inline=False)
    embed.add_field(name="**Pega Stats**", value="*Fire*: " + str(json_data['fire']) + "\n *Wind*: " + str(json_data['wind']) + "\n *Speed*: " + str(json_data['speed']) + "\n *Water*: " + str(json_data['water']) + "\n *Strength*: " + str(json_data['strength']) + "\n *Lightning*: " + str(json_data['lightning']), inline=False)
    embed.add_field(name="**Owner Address**", value=str(json_data['ownerAddress']), inline=False)
    embed.set_footer(text="Created By: Renzxc#6896")
    await ctx.send(embed=embed)

@client.command()
async def renthistory(ctx, arg):
    response_g = requests.get("https://api-apollo.pegaxy.io/v1/game-api/pega/" + arg)
    json_data_g = json.loads(response_g.text)
    response = requests.get("https://api-apollo.pegaxy.io/v1/game-api/rent/history/" + arg)
    json_data = json.loads(response.text)
    embed=discord.Embed(
    title="#"+ arg +"  **" + str(json_data_g['pega']['name'])+"**",
        url="",
        description="",
        color=discord.Color.blue())
    embed.set_thumbnail(url=str(json_data_g['pega']['design']['avatar_2']))
    if json_data['history']:
      for x in json_data['history']:
        string = "*Rent Mode*: `" + str(x['rentMode'])
        if str(x['rentMode']) == "PAY_RENT_FEE":
          string = string+ "` | *Rent Duration*: `" + display_time(int(x['rentDuration']))
        else:
          string = string + "` | *Scholar Share*: `" + str(int(x['price'])/10000) + "%"
        date_time = datetime.datetime.fromtimestamp(int(x['rentAt']))
        string = string + "` | *Date Rented*: `" + str(date_time)
        string = string + "` | *Renter Address*: `" + str(x['renter']['address']) + "`"
        embed.add_field(name="**Rent History**", value=string, inline=False)
    embed.set_footer(text="Created By: Renzxc#6896")
    await ctx.send(embed=embed)

@client.command()
async def racehistory(ctx, arg):
    response_g = requests.get("https://api-apollo.pegaxy.io/v1/game-api/pega/" + arg)
    json_data_g = json.loads(response_g.text)
    response_h = requests.get("https://api-apollo.pegaxy.io/v1/game-api/rent/history/" + arg)
    json_data_h = json.loads(response_h.text)
    response = requests.get("https://api-apollo.pegaxy.io/v1/game-api/race/history/pega/" + arg)
    json_data = json.loads(response.text)
    embed=discord.Embed(
    title="#"+ arg +"  **" + str(json_data_g['pega']['name'])+"**",
        url="",
        description="",
        color=discord.Color.blue())
    embed.set_thumbnail(url=str(json_data_g['pega']['design']['avatar_2']))

    gold = 0
    silver = 0
    bronze = 0
    vis = 0
    goldt = 0
    silvert = 0
    bronzet = 0
    vist = 0
    goldy = 0
    silvery = 0
    bronzey = 0
    visy = 0
    visscho = 0
    visowner = 0

    if json_data['data']:
      for x in json_data['data']:
        date_time_raw = datetime.datetime.fromtimestamp(int(x['race']['end']))
        old_timezone = pytz.timezone("UTC")
        new_timezone = pytz.timezone("Asia/Manila")
        current_time = datetime.datetime.now(new_timezone)
        yesterday = current_time - datetime.timedelta(1)
        date_time = old_timezone.localize(date_time_raw).astimezone(new_timezone)
        
        if int(x['position']) == 1:
          gold = gold + 1
        elif int(x['position']) == 2:
          silver = silver + 1
        elif int(x['position']) == 3:
          bronze = bronze + 1
        vis = vis + int(x['reward'])
        
        if date_time.strftime('%m/%d/%Y') == current_time.strftime('%m/%d/%Y'):
          if int(x['position']) == 1:
            goldt = goldt + 1
          elif int(x['position']) == 2:
            silvert = silvert + 1
          elif int(x['position']) == 3:
            bronzet = bronzet + 1
          vist = vist + int(x['reward'])
          visowner = visowner + int(x['reward'])
          
        if date_time.strftime('%m/%d/%Y') == yesterday.strftime('%m/%d/%Y'):
          if int(x['position']) == 1:
            goldy = goldy + 1
          elif int(x['position']) == 2:
            silvery = silvery + 1
          elif int(x['position']) == 3:
            bronzey = bronzey + 1
          visy = visy + int(x['reward'])
    if json_data_h['history']:
      percent = int(json_data_h['history'][0]['price'])/10000
    else:
      percent = 0
    visscho = (visowner/100) * percent

    embed.add_field(name="**Last 100 Races**", value="*Gold*: " + str(gold) + "\n*Silver*: " + str(silver) + "\n*Bronze*: " + str(bronze) + "\n*$VIS Earned*: **" + str(vis) + "**", inline=False)
    embed.add_field(name="**Today's Earnings** __" + current_time.strftime('%b, %d %Y') + "__", value="*Gold*: " + str(goldt) + "\n*Silver*: " + str(silvert) + "\n*Bronze*: " + str(bronzet) + "\n*$VIS Earned*: **" + str(vist) + "**", inline=False)
    if json_data_h['history']:
      if str(json_data_h['history'][0]['rentMode']) == "SHARE_PROFIT":
        embed.add_field(name="**Shared Profit Today** __" + current_time.strftime('%b, %d %Y') + "__", value="*$VIS Earned(Owner)*: " + str(visowner - visscho) + "\n*$VIS Earned(Scholar)*: **" + str(visscho) + "** (" + str(percent) + "%)\n*Energy*: " + str(json_data_g['pega']['energy']) + "/25", inline=False)
    embed.add_field(name="**Yesterday's Earnings** __" + yesterday.strftime('%b, %d %Y') + "__", value="*Gold*: " + str(goldy) + "\n*Silver*: " + str(silvery) + "\n*Bronze*: " + str(bronzey) + "\n*$VIS Earned*: **" + str(visy) + "**", inline=False)
    
    embed.set_footer(text="Created By: Renzxc#6896")
    await ctx.send(embed=embed)

@client.command()
async def assets(ctx, arg):
    response = requests.get("https://api-apollo.pegaxy.io/v1/pegas/owner/user/" + arg)
    json_data = json.loads(response.text)
    embed=discord.Embed(
    title="**Assets**",
        url="",
        description="",
        color=discord.Color.blue())
    totalassets = 0
    count = 1
    pegaid = ""
    embc = 1

    for x in json_data:
      if embc != 24:
        totalassets = count
        embed.add_field(name="**" + str(count) + ". "+ str(x['name']) +"**", value="*Pega ID*: `" + str(x['id']) + "`\n*Energy*: `" + str(x['energy']) + "`\n*Rent Type*: `" + str(x['lastRenterRentMode']) + "`\n*Scholar*: `" + str(x['lastRenterIsDirect']) + "`", inline=False)
        count = count + 1
        if int(x['energy']) >= 20:
          pegaid = pegaid + " `#" + str(x['id']) + "` "
      
    embed.add_field(name="**Total Assets**", value="*Count*: " + str(totalassets), inline=False)
    if pegaid != "#":
      embed.add_field(name="**Pega ID of 20 energy and above**", value="*Pega ID(s)*: " + str(pegaid), inline=False)
    embed.set_footer(text="Created By: Renzxc#6896")
    await ctx.send(embed=embed)

@client.command()
async def locked(ctx, arg):
    response = requests.get("https://api-apollo.pegaxy.io/v1/assets/count/user/" + arg)
    json_data = json.loads(response.text)
    embed=discord.Embed(
    title="**Locked $VIS** of `" + arg + "` **address**",
        url="",
        description="",
        color=discord.Color.blue())
    current_time = datetime.datetime.now(pytz.timezone("Asia/Manila"))
    embed.add_field(name="**Details**", value="*$VIS*: `" + str(json_data['lockedVis']) + "` \n*As of*: **" + current_time.strftime('%b, %d %Y, %H:%M:%S') + "**", inline=False)
    embed.set_footer(text="Created By: Renzxc#6896")
    await ctx.send(embed=embed)

@client.command()
async def vis(ctx, arg = None):
    current_time = datetime.datetime.now(pytz.timezone("UTC"))
    response = ""
    if str(arg).casefold() == "all":
      response = requests.get("https://pegaxy-api.herokuapp.com/api/v1/historical/vis/burn-mint?from=")
    elif arg is None:
      time_arg = current_time - datetime.timedelta(1)
      response = requests.get("https://pegaxy-api.herokuapp.com/api/v1/historical/vis/burn-mint?from=" + time_arg.strftime('%Y-%m-%d') + "T00%3A00%3A00")
    json_data = json.loads(response.text)
    embed=discord.Embed(
    title="**MINT : BURN** *ratio*",
        url="",
        description="",
        color=discord.Color.blue())
    if str(arg).casefold() == "all":
      burns = 0
      for x in json_data['burned']:
        burns = burns + x['amount']
      mints = 0
      for x in json_data['minted']:
        mints = mints + x['amount']
      ratios = (burns / mints) * 100
      embed.add_field(name="**Total**", value="*Minted*: **" + str(mints) + "**\n*Burned*: **" + str(burns) + "**\n*Ratio*: **" + str(math.ceil(ratios)) + "%**", inline=False)
    elif arg is None:
      burnt = int(json_data['burned'][1]['amount'])
      burny = int(json_data['burned'][0]['amount'])
      mintt = int(json_data['minted'][1]['amount'])
      minty = int(json_data['minted'][0]['amount'])
      ratiot = (burnt / mintt) * 100
      ratioy = (burny / minty) * 100
      ratioa = ((burny + burnt) / (minty + mintt)) * 100

      embed.add_field(name="**Today** " + "__" + current_time.strftime('%b, %d %Y') + "__", value="*Minted*: **" + str(minty) + "**\n*Burned*: **" + str(burnt) + "**\n*Ratio*: **" + str(math.ceil(ratiot)) + "%**", inline=False)
      embed.add_field(name="**Yesterday** " + " __" + (current_time - datetime.timedelta(1)).strftime('%b, %d %Y') + "__", value="*Minted*: **" + str(minty) + "**\n*Burned*: **" + str(burny) + "**\n*Ratio*: **" + str(math.ceil(ratioy)) + "%**", inline=False)
      embed.add_field(name="**Today and Yesterday**", value="*Minted*: **" + str(minty + mintt) + "**\n*Burned*: **" + str(burny + burnt) + "**\n*Ratio*: **" + str(math.ceil(ratioa)) + "%**", inline=False)
    embed.set_footer(text="Note: Date is UTC based \n\nCreated By: Renzxc#6896")
    await ctx.send(embed=embed)

@client.command()
async def paginate(ctx):
        embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
        embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
        embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3]
        await paginator.run(embeds)

@client.command()
async def vhelp(ctx):
    embed=discord.Embed(
    title="**HELP**",
        url="",
        description="",
        color=discord.Color.blue())

    embed.add_field(name="**Commands**", value="`/pega <id>`: *pega details*\n`/renthistory <id>`: *renting history*\n`/racehistory <id>`: *racing history*\n`/assets <address>`: *list of your assets with details*\n`/locked <address>`: *locked $vis of the address*\n`/vis`: *mint : burn ratio for yesterday and today*\n`/vis all`: *all time mint : burn ratio*", inline=False)
    await ctx.send(embed=embed)
    
my_secret = os.environ['TOKEN']
client.run(my_secret)