import random
from PIL import Image
from FallenRobot import telethn as neko
from telethon import events
@neko.on(events.NewMessage(pattern="/wish ?(.*)"))
async def wish(e):

 if e.is_reply:
         mm = random.randint(1,100)
         lol = await e.get_reply_message()
         fire = "https://telegra.ph/file/6f20fbac47ad0f0196588.jpg"
         await neko.send_file(e.chat_id, fire,caption=f"**Hey [{e.sender.first_name}](tg://user?id={e.sender.id}), Your wish has been cast.💜**\n\n__chance of success {mm}%__", reply_to=lol)
 if not e.is_reply:
         mm = random.randint(1,100)
         fire = "https://telegra.ph/file/065b18d37a25206190fab.jpg"
         await neko.send_file(e.chat_id, fire,caption=f"**Hey [{e.sender.first_name}](tg://user?id={e.sender.id}), Your wish has been cast.💜**\n\n__chance of success {mm}%__", reply_to=e)




__help__ = """
× ʜᴇʀᴇ wish ᴍᴏᴅᴜʟᴇ use /wish and say anything 
 __if you need reading some hindi shayari so use__ /shayari __and see__×
"""

__mod_name__ = "WISH"
