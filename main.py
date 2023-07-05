import discord, aiohttp, asyncio, re, json
from urlextract import URLExtract
limiteds = []
UrlExtractor = URLExtract()
client = discord.Client()
with open('settings.json', "r") as f:
    config = json.load(f)
async def getiteminfo(assetid, ping):
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "Accept-Encoding": "gzip", "Cache-Control": "max-age=0"}) as session:
        async with session.get(f"https://economy.roblox.com/v2/assets/{assetid}/details") as response:
            itemdata = await response.json()
            itemthumbnail = None
            async with session.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={assetid}&returnPolicy=PlaceHolder&size=700x700&format=Png&isCircular=false") as response:
                itemthumbnail = (await response.json())["data"][0]["imageUrl"]
            async with session.post(config.get("webhook"), json={"content":ping,"embeds":[{"title":itemdata.get("Name"),"author":{"name":itemdata.get("Creator").get("Name"), "url":f'https://www.roblox.com/{itemdata.get("Creator").get("CreatorType").lower()}s/{itemdata.get("Creator").get("CreatorTargetId")}'},"thumbnail":{"url":itemthumbnail},"url":f"https://www.roblox.com/catalog/{assetid}","color":0x682CEB,"fields":[{"name": "AssetType", "value": f'{config.get("useless").get(str(itemdata.get("AssetTypeId")))}'},{"name":"Price","value":f'{itemdata.get("PriceInRobux")}'},{"name":"Quantity","value":f'{itemdata.get("Remaining")}'}]}],"username":"Possible Items", "avatar_url":"https://i.imgur.com/KBswCsd.png"}) as response:
                return
@client.event
async def on_message(message):
    global limiteds
    if message.channel.id in config.get("notifierchannels"):
        item = ((message.embeds[0].url).split("/"))[4]
        await getiteminfo(item, config.get("role"))
    urls = UrlExtractor.find_urls(message.content)
    for urll in urls:
        if "/catalog/" in urll:
            item = re.findall("\d+", urll)[0]
            if item not in limiteds:
                limiteds.append(item)
                await getiteminfo(item, config.get("probablyrole"))
asyncio.run(client.start(config.get("token")))