from pyrogram import filters
from FallenRobot.modules.mongo.sangmata_db import *
from FallenRobot import pbot as app
from FallenRobot.Pyro.permissions import adminsOnly
from FallenRobot.Pyro.message_utils import kirimPesan

user_data = {}

# Check user that changes first_name, last_name, and username
@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=3)
async def cek_mataa(_, m):
    if not await is_sangmata_on(m.chat.id):
        return

    chat_id = m.chat.id
    user_id = m.from_user.id

    if chat_id not in user_data:
        user_data[chat_id] = {}

    if user_id not in user_data[chat_id]:
        user_data[chat_id][user_id] = {
            "username": m.from_user.username,
            "first_name": m.from_user.first_name,
            "last_name": m.from_user.last_name,
        }
    else:
        username = user_data[chat_id][user_id]["username"]
        first_name = user_data[chat_id][user_id]["first_name"]
        last_name = user_data[chat_id][user_id]["last_name"]
        msg = ""

        if username != m.from_user.username or first_name != m.from_user.first_name or last_name != m.from_user.last_name:
            msg += "👀 <b>Imposter Detected</b>\n\n"

        if username != m.from_user.username:
            msg += f"❇️ {m.from_user.mention} [<code>{m.from_user.id}</code>] changed username from @{username} to @{m.from_user.username}.\n"
            user_data[chat_id][user_id]["username"] = m.from_user.username

        if first_name != m.from_user.first_name:
            msg += f"❇️ {m.from_user.mention} [<code>{m.from_user.id}</code>] changed first Name from {first_name} to {m.from_user.first_name}.\n"
            user_data[chat_id][user_id]["first_name"] = m.from_user.first_name

        if last_name != m.from_user.last_name:
            msg += f"❇️ {m.from_user.mention} [<code>{m.from_user.id}</code>] changed last name from {last_name} to {m.from_user.last_name}."
            user_data[chat_id][user_id]["last_name"] = m.from_user.last_name

        if msg != "":
            await kirimPesan(m, msg, quote=True)


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
            await kirimPesan(m, "Imposter Detection enabled in your group. I will track name and username changes in this chat. If a user changes their name and username, I will send a message showing any related changes")
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

*• /detectimposter:* Use this command to track name and username changes in the group. If a user changes their name and username, the bot will send a message showing any related changes.
"""
