import os
import subprocess
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from FallenRobot import pbot as pgram

DEV_USERS = (1143358497, 2033411815, 5667156680)

@pgram.on_message(filters.command(["update"]) & filters.user(DEV_USERS))
async def _gitpull(client, message):
    m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if str(m[0]) != "A":
        x = await message.reply_text("» ғᴇᴛᴄʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ғʀᴏᴍ ʀᴇᴩᴏ ᴀɴᴅ ᴛʀʏɪɴɢ ᴛᴏ ʀᴇsᴛᴀʀᴛ...")
        return os.system(f"kill -9 {os.getpid()} && python3 -m FallenRobot")
    else:
        await message.reply_text(f"» Testing ɪs ᴀʟʀᴇᴀᴅʏ ᴜᴩ-ᴛᴏ-ᴅᴀᴛᴇ !")

@pgram.on_message(filters.command("logs") & filters.user(DEV_USERS))
async def _logs(client, message):
    x = subprocess.getoutput("tail log.txt")
    link = await paste(x)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Open", url=link),
                                      InlineKeyboardButton("Send", callback_data="send_logs")]])
    await message.reply_text(link, reply_markup=keyboard)

@pgram.on_callback_query(filters.regex("send_logs"))
async def semdd(_, query):
    await query.message.edit("**Sent Logs as file**")
    await _.send_document(query.message.chat.id, "log.txt")
