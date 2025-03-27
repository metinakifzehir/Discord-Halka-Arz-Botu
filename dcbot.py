import nextcord
from nextcord.ext import commands

BOT_TOKEN = "bot_token"
CHANNEL_ID = "channel_id"

intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents= intents)


@bot.event
async def on_ready():
    infile = open("yeni.txt", 'r', encoding="utf-8")
    lines = ""
    key = 0
    for line in infile:
        lines += line
    for c in lines:
        if c.isprintable():
            key = 1
    if key == 1:
        lines = "\n" + lines
        retStr = str("""```ansi\n{}```""".format(lines))
        print(retStr)
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(retStr)
    await bot.close()

bot.run(BOT_TOKEN)
