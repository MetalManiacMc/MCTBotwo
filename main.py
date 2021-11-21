import json
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [906169345007304724]

def lowerIt(string):
    out=""
    for i in source[key]:
            if ord("Z") >= ord(i) >= ord("A"):
                out += chr(ord(i) + 32)
            else:
                out += i
    return out
    
def translater(string, target, source):
    source = json.load(open("lang/"+source+".json"))
    target = json.load(open("lang/"+target+".json"))
    
    for key in source: #try to match exactly with lowercase
        if lowerIt(source[key]) == lowerIt(string):
            return target[key]
        
    listreturn = []
    for key in source: #lowercase keyword match check
        if lowerIt(string) in lowerIt(source[key]):
            listreturn.append(target[key])
    
    try: #this try except is here because i have a small expectation of error...
        if len(listreturn) > 0:
            return "Unexact matches: "+"|".join(listreturn)
    except:
        return "Something went wrong with list length checking..."
    
    return "Invalid string"

def fetch_translation(target, string):
    t = json.load(open(f"lang/{target}.json")) 
    key = f"{string}"
    return t.get(key)

@slash.slash(name="translate",
             description="Returns the translation found in-game for a string",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="string",
                     description="The string or key to translate.",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="target",
                     description="Language code, in which the string is going to be sent. EX: es_es",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="sourcelang",
                     description="'key' or language code, in which the string is going to be retrieved. EX: fr_fr, key",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def translate(ctx, string, target,  sourcelang = "en_us"):
    if sourcelang == "key":
        await ctx.send(fetch_translation(target, string))
    else:
        await ctx.send(translater(string, target, sourcelang))

client.run(open("token.txt").read())
