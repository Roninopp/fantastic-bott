from pyrogram import filters
from datetime import datetime
import pytz
from pytz import timezone
from html import escape
from FallenRobot.modules.mongo.sangmata_db import *
from FallenRobot import pbot as app
from FallenRobot.Pyro.permissions import adminsOnly
from FallenRobot.Pyro.message_utils import kirimPesan
from FallenRobot.utils.mongo import db as dbname
import re

async def get_name_change_history(user_id: int):
    user = await matadb.find_one({"user_id": user_id})
    return user.get("name_changes", [])

async def cek_mataa(_, m):
    if not await is_sangmata_on(m.chat.id):
        return
    if not await cek_userdata(m.from_user.id):
        await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
    else:
        username, first_name, last_name = await get_userdata(m.from_user.id)
        msg = ""
        old_user = await app.get_chat_member(m.chat.id, m.from_user.id)
        if username != m.from_user.username or first_name != m.from_user.first_name or last_name != m.from_user.last_name:
            msg += "👀 <b>Imposter Detected</b>\n\n"
        if username != m.from_user.username:
            msg += f"❇️ {m.from_user.mention} [<code>{m.from_user.id}</code>] changed username from @{username} to @{m.from_user.username}.\n"
            await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
        if first_name != m.from_user.first_name:
            msg += f"❇️ {m.from_user.mention} [<code>{m.from_user.id}</code>] changed first Name from {first_name} to {m.from_user.first_name}.\n"
            await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
        if last_name != m.from_user.last_name:
            msg += f"❇️ {m.from_user.mention} [<code>{m.from_user.id}</code>] changed last name from {last_name} to {m.from_user.last_name}.\n"
            await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
        if msg != "":
            await kirimPesan(m, msg, quote=True)

import re

@app.on_message(filters.group & filters.command("history") & ~filters.bot & ~filters.via_bot)
async def search_history(_, m):
    if len(m.command) == 1:
        return await kirimPesan(m, f"Please provide a user ID or username to search the history.")
    query = m.command[1].strip()
    user_id = None
    if query.startswith("@"):
        username = query[1:]
        try:
            user_id = (await app.get_users(username)).id
        except:
            await kirimPesan(m, f"User with username '{username}' not found.")
    elif re.match(r"^\d+$", query):
        user_id = int(query)
    if user_id is None:
        return await kirimPesan(m, f"Invalid user ID or username. Please provide a valid user ID or username to search the history.")

    if await cek_userdata(user_id):
        username, first_name, last_name = await get_userdata(user_id)
        history_msg = "<b>🔰 Name History:</b>\n\n"
        history_msg += f"<code>👤 {user_id}</code>\n\n"

        name_history = await history_db.find({"user_id": user_id}).sort("_id", -1).to_list(None)

        for i, history in enumerate(name_history, start=1):
            timestamp = history["_id"].generation_time.astimezone(pytz.timezone("Asia/Kolkata"))
            formatted_timestamp = timestamp.strftime("[<code>%d/%m/%Y %I:%M:%S %p</code>]")
            change_first_name = escape(history["first_name"])
            change_last_name = escape(history["last_name"]) if history["last_name"] is not None else ""
            history_msg += f"<code>{i}.</code> {formatted_timestamp}\n"
            history_msg += f"   <code>{change_first_name}</code> <code>{change_last_name}</code>\n"

            if history["username"]:
                change_username = escape(history["username"])
                history_msg += f"   @{change_username}\n"

            history_msg += "\n"

        await kirimPesan(m, history_msg, quote=True)
    else:
        await kirimPesan(m, "User data not found.")
        

@app.on_message(filters.group & filters.command("detectimposter") & ~filters.bot & ~filters.via_bot)
@adminsOnly("can_change_info")
async def set_mataa(_, m):
    if len(m.command) == 1:
        return await kirimPesan(m, f"Use <code>/{m.command[0]} on</code>, to enable Imposter Detection. If you want to disable, you can use off parameter.")
    if m.command[1] == "on":
        cekset = await is_sangmata_on(m.chat.id)
        if cekset:
            await kirimPesan(m, "Imposter Detection already enabled in your group.")
        else:
            await sangmata_on(m.chat.id)
            await kirimPesan(m, "Imposter Detection enabled in your group. I will track name and username changes in this chat. If user change their name and username, I will send a message showing any related changes")
    elif m.command[1] == "off":
        cekset = await is_sangmata_on(m.chat.id)
        if not cekset:
            await kirimPesan(m, "Imposter Detection already disabled in your group.")
        else:
            await sangmata_off(m.chat.id)
            await kirimPesan(m, "Imposter Detection has been disabled in your group.")
    else:
        await kirimPesan(m, "Invalid command, Use <code>/detectimposter on/off</code> to enable or disable Imposter Detection in your chat.")


__mod_name__ = "ɪᴍᴘᴏsᴛᴇʀ ᴅᴇᴛᴇᴄᴛɪᴏɴ"
__help__ = """
*• /detectimposter:* Use this command to track name and username changes in the group. If a user changes their name and username, the bot will send a message showing any related changes.

*• /history:* Reply to a user with this command to get their previous name changes history.
"""
