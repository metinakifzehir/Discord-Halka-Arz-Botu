import nextcord
from nextcord.ext import commands

BOT_TOKEN = "MTE4MjY5OTkzNjEwNjY3NjI0NA.G-_fRQ.aPitLhQHoDpTJaoseAcAnERrpy617-mQhoEO1U"
CHANNEL_ID = 1182820757584232499
#CHANNEL_ID = 792402432293601291

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

"""
@tasks.loop(hours=24)  # 24 saate bir çalışacak
async def send_daily_message():
    now = datetime.now()
    if now.hour == 20 and now.minute == 0:
        channel_id = 792402432293601291  # Kanal ID'sini buraya ekleyin
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send("Her gün saat 20:00'de gönderilen mesaj!")
        else:
            print(f"Belirtilen kanal ID'si geçersiz: {channel_id}")
"""

bot.run(BOT_TOKEN)
