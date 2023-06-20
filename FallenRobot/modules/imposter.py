from pyrogram import filters
from datetime import datetime
from pytz import timezone
from html import escape
from FallenRobot.modules.mongo.sangmata_db import *
from FallenRobot import pbot as app
from FallenRobot.Pyro.permissions import adminsOnly
from FallenRobot.Pyro.message_utils import kirimPesan


async def get_name_change_history(user_id: int):
    user = await matadb.find_one({"user_id": user_id})
    return user.get("name_changes", [])
    
# Check user that change first_name, last_name and username
@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=3)
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

    # Check if the command is /history
    if m.text and m.text.startswith("/history"):
        user_id = m.reply_to_message.from_user.id if m.reply_to_message else m.from_user.id
        if await cek_userdata(user_id):
            username, first_name, last_name = await get_userdata(user_id)
            history_msg = f"🔰 <b>Name History:</b>\n\n"
            history_msg += f"👤 {user_id}\n\n"

            name_changes = await get_name_change_history(user_id)

            if name_changes:
                for idx, change in enumerate(name_changes, 1):
                    change_username = escape(change["username"])
                    change_first_name = escape(change["first_name"])
                    change_last_name = escape(change["last_name"]) if change["last_name"] else "None"
                    change_date = datetime.fromtimestamp(change["timestamp"], tz=timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")
                    change_description = escape(change["description"])

                    history_msg += f"{idx}. {change_date} {change_first_name} {change_last_name} - {change_description}\n"
            else:
                history_msg += "No name change history found for this user."

            await kirimPesan(m, history_msg, quote=True)


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


__mod_name__ = "𝙳ᴇᴛᴇᴄᴛ 𝙸ᴍᴘᴏsᴛᴇʀ"
__help__ = """

*• /detectimposter:* Use this command to track name and username changes in group. If user change their name and username, I will send a message showing any related changes.
"""
