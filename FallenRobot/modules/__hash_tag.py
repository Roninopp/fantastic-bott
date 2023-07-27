import requests
from bs4 import BeautifulSoup as  BSP
from FallenRobot import pbot as mukesh
from pyrogram import filters
url = "https://all-hashtag.com/library/contents/ajax_generator.php"

@mukesh.on_message(filters.command("hastag"))
async def hastag(bot, message):
    global content
    try:
        text = message.text.split(' ',1)[1]
        data = dict(keyword=text, filter="top")

        res = requests.post(url, data).text

        content = BSP(res, 'html.parser').find("div", {"class":"copy-hashtags"}).string
    except IndexError:
        return await message.reply_text("Example:\n\n`/hastag python`")
        
    
    await message.reply_text(f"𝐇𝐄𝐑𝐄 𝐈𝐒 𝐘𝐎𝐔𝐑 𝐇𝐀𝐒𝐓𝐀𝐆:\n<pre>{content}</pre>", quote=True)
    
