import interactions as di
import json
from cogs.variables import *


def complete(search:str, inside:list):

    """
    This function is essentially an autocompletion.
    It takes a string and a list, in which it"s going to find complete strings.
    Walks through the list and asks whether the search is in the value. If it is,
    it appends the value to result. If none are found, it returns an empty list.
    """

    return [i for i in inside if search.lower() in i.lower()]


def fetch_default(code, category, data):
    """
    This function fetches defaults in serverdefaults.json
    """
    f = json.load(open("serverdefaults.json"))
    return f[code][category][data]


def find_translation(string:str, targetlang:str, sourcelang:str, edition:str, page:int=1, pagesize:int=10):

    """
    This function finds translations and returns the list of matches.
    """
    string = string.lower()
    try:
        if targetlang!="key": # if either are key, they should not be searched for as files, instead use jsdef
            jstarget = open_json(lang(targetlang, edition), edition)
        if sourcelang!="key":
            jssource = open_json(lang(sourcelang, edition), edition)
        jsdef = open_json("en_us") # this will get used everytime to key or from key is used... (json default... change the name if you want)
    except IndexError:
        return

    exact=None
    if targetlang=="key": # figures out, which mode to use
        if sourcelang=="key":
            result = complete(string, jsdef) #ktk
        else:
            result = [i for i in jsdef if string in jssource[i].lower()] #stk
            for i in result:
                if jssource[i].lower()==string:
                    exact=i
                    break
    else:
        if sourcelang=="key":
            result = [jstarget[i] for i in complete(string, jsdef)] #kts
            try: exact=jstarget[string]
            except: pass
        else:
            result = [jstarget[i] for i in [i for i in jssource if string in jssource[i].lower()]] #sts(string, jstarget, jssource)
            for i in jssource:
                if jssource[i].lower()==string:
                    exact=jstarget[i]
                    break

    reslen=len(result)
    added=False
    cut=False
    if len(result)>10:
        result=result[10*(page-1):pagesize*page]
        added=True
    n=len(result)
    if page==1:
        resfull="|".join(result)
        while not cut:
            if len(resfull)>1000:
                result=result[:-1]
                resfull="|".join(result)
                added=True
                n-=1
            else:
                cut=True
    try:
        while True:
            result.remove("")
            n-=1
    except ValueError:
        pass

    if added:
        buttons = di.ActionRow.new(prevbutton, nextbutton)
    else:
        buttons=None

    pagenum=int(reslen/n) + (reslen % n>0)


    if added:
        result.append("**…and more!**")
    return result, exact, buttons, pagenum


def lang(search:str, edition):

    """
    Returns a complete internal language code to be used for file opening.
    Input can be the expected output too.
    Input can be approved language code, name, region or internal code (searching in this order)
    """
    search = search.lower()
    injava=False
    if edition=="java":
        for i in range(len(langcodesapp)): # We can't use complete here because we would have no clue which langcode to use. The thing we need is index of langcode, not completed langname or whatever.
            if search in langcodesapp[i].lower():
                return langcodes[i]
        for i in range(len(langcodes)):
            if search in langcodes[i].lower():
                return langcodes[i]
        for i in range(len(langnames)):
            if search in langnames[i].lower():
                return langcodes[i]
        for i in range(len(langregions)):
            if search in langregions[i].lower():
                return langcodes[i]
        for i in range(len(langfull)):
            if search in langfull[i].lower():
                return langcodes[i]
    elif edition=="bedrock":
        for i in range(len(belangcodes)): # We can't use complete here because we would have no clue which langcode to use. The thing we need is index of langcode, not completed langname or whatever.
            if search in belangcodes[i].lower():
                return belangcodes[i]
        for i in range(len(belangnames)):
            if search in belangnames[i].lower():
                return belangcodes[i]
        for i in range(len(belangregions)):
            try:
                if search in belangregions[i].lower():
                    return belangcodes[i]
            except AttributeError:pass
        for i in range(len(langfull)):
            if search in langfull[i].lower():
                injava=True
                for x in range(len(belangcodes)):
                    if langcodes[i]==belangcodes[x]:
                        return belangcodes[x]
                    
            
    ret=complete(search, langcodes)
    if len(ret)>0:
        return ret[0]
    else:
        if injava==False:
            raise embederr("Language not found…")
        elif injava==True:
            raise embederr("This language does not exist in Bedrock Edition.")

def get_pagenum(embed):
    pagenum=embed.footer.text
    pagenum=pagenum.split("/")
    pagenum=pagenum[0].split(" ")
    pagenum=pagenum[1]
    return int(pagenum)


async def lang_autocomplete(ctx: di.CommandContext, value: str = ""):
    items = langfull
    choices = [
        di.Choice(name=item, value=item) for item in items if value.lower() in item.lower()
    ] 
    await ctx.populate(choices[:25])