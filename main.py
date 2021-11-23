import json
import os
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
path="C:\\Users\\matej\\Desktop\\" #full path for debug. can be a blank string.
debug=False #True if you are on your pc and don't want to turn the bot on

for a, b, c in os.walk(path+"lang"): #Gives a list of language codes, so i can search in them
    filenames=c
    break
langcodes=[]
for i in filenames:
    langcodes.append(i.split(".")[0])


        

guild_ids = [906169345007304724]
@client.event
async def on_ready():
    print("Online!")


def finder(search,inside=langcodes,outputlist=False,isdictionary=False): #returns list of found searches inside a list (by default, searches in langcodes)
    o=[]
    if not isdictionary:
        for i in inside:
            if search.lower() in i.lower():
                if outputlist:
                    o.append(i)
                else:
                    return i
    else: #I believe that a problem is here... i don't know how can i not check for values in disctionary or something...
        for i in inside:
            if search in inside[i].lower():
                if outputlist:
                    o.append(i)
                else:
                    return i

    if outputlist:
        return o
    else:
        return search
                
    
def unpacker(string, target, source, fetch=True): #finds string's key in source language and puts it to the fetcher or return it
    try: #tries to open source language file. we searched for the codes earlier in the code, so it should be ok
        file = json.load(open(path+"lang/"+source+".json"))
    except:
        return f"Source language {source} was not found."
    
    for key in file: #tries to match exactly with lowercase
        if file[key].lower() == string:
            if fetcher:
                return fetcher(key,target)
            else:
                return key
    
    keys=[] #will return a list of unexact matches
    for key in finder(string,file,True,True):
        keys.append(key)
    if fetch:
        return fetcher(keys,target,True)
    else:
        return keys
    


def fetcher(key, target, islist=False): #finds a translation based on a key and target language
    try:
        return f"Found {json.load(open(path+f'lang/{target}.json'))[key]} in {target}." #changed .get() for [] bc we want an error raised, not None value | returns when matching exactly
    except: #my fallback fetcher
        try:
            file=json.load(open(path+f"lang/{target}.json"))
        except:
            return f"Target language {target} was not found."

        if not islist: #here was return found file[key] in target, but wouldn't be activated, so i removed it
            keys=[] #will return a list of unexact matches
            for i in finder(key,file,True):
                keys.append(i)
        else: #this should activate only if we already have a list in key
            keys=key
        
        strings=[]
        for i in keys:
            strings.append(file[i])
        
        if len(strings) > 1: #joins list or outputs one string
            return "Unexact matches: '"+"', '".join(strings)+"' in "+target
        elif len(strings) > 0:
            return f"Unexact match: '{strings[0]}' in "+target
        
    print(key,target,keys) #the final return fallback. was: "Invalid string"
    return f"Did not find the {key} key in {target}."
                    

    
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
                     name="source",
                     description="'key' or language code, in which the string is going to be retrieved. EX: fr_fr, key",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def translate(ctx, string, target, source = "en_us"): #moved out the googler bc it made the debugging a lot easier for me and does not change a thing
    await ctx.send(google(string,target,source))
def google(string, target,  source = "en_us"):
    if source == "key":
        return fetcher(string.lower(), finder(target.lower()))
    else:
        return unpacker(string.lower(), finder(target.lower()), finder(source.lower()))




while debug:#this runs when you want to test this offline
    print(translate(input("string: ").lower(), finder(input("target: ").lower()), finder(input("source: ").lower())))

client.run(open(path+"token.txt").read())
