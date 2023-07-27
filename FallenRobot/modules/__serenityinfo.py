
from FallenRobot import pbot as app
from pyrogram import filters, types as okok

msg = """
Serenity Is a Advanaced Anti-Spam Cymatic Scanner based on API
Created and developed For removing toxic people from telegram
𖣘 It can protecc you from potential threats on telegram.
𖣘 You can request gban/scan for anyone in our Support Group
𖣘 Team Samurai can be connected with any bots
"""

@app.on_message(filters.command(["serenity"]))
async def OKOKKKKK(_,message):
        global msg
        await message.reply_photo("https://telegra.ph/file/b2920fd6634ca6a90b9e9.jpg",caption=msg,reply_markup=okok.InlineKeyboardMarkup(
                           [
                            [
                             okok.InlineKeyboardButton(text="Serenity Bot",url="t.me/Serenity_SystemBot"),
                             okok.InlineKeyboardButton(text="Appeal",url="t.me/Serenity_Support")
                            ],
                            [
                             okok.InlineKeyboardButton(text="Serenity Logs",url="t.me/Serenity_Log"),
                             okok.InlineKeyboardButton(text="Serenity Updates",url="t.me/SerenityUpdates")
                            ]
                           ]
 ))



__mod_name__ = "ꜱᴇʀᴇɴɪᴛʏ-ꜱʏꜱ"

__help__ = """
 ➩ /serenity : Serenity Is A Gban System Use This Command To See Full Information
 """
