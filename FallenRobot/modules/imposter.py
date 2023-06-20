from pyrogram import filters
from FallenRobot.modules.mongo.sangmata_db import *
from FallenRobot import pbot as app
from FallenRobot.Pyro.permissions import adminsOnly
from FallenRobot.Pyro.message_utils import kirimPesan


async def send_name_change_message(chat_id, user, username, first_name, last_name):
    msg = ""
    old_user = await app.get_chat_member(chat_id, user.id)
    if username != user.username or first_name != user.first_name or last_name != user.last_name:
        msg += "👀 <b>Imposter Detected</b>\n\n"
    if username != user.username:
        msg += f"❇️ {user.mention} [<code>{user.id}</code>] changed username from @{username} to @{user.username}.\n"
        await add_userdata(user.id, user.username, user.first_name, user.last_name)
    if first_name != user.first_name:
        msg += f"❇️ {user.mention} [<code>{user.id}</code>] changed first Name from {first_name} to {user.first_name}.\n"
        await add_userdata(user.id, user.username, user.first_name, user.last_name)
    if last_name != user.last_name:
        msg += f"❇️ {user.mention} [<code>{user.id}</code>] changed last name from {last_name} to {user.last_name}."
        await add_userdata(user.id, user.username, user.first_name, user.last_name)
    if msg != "":
        chat = await app.get_chat(chat_id)
        await kirimPesan(chat, msg, quote=True)


# Check user that change first_name, last_name and username
@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=3)
async def cek_mataa(_, m):
    if not await is_sangmata_on(m.chat.id):
        return
    if not await cek_userdata(m.from_user.id):
        await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
    else:
        username, first_name, last_name = await get_userdata(m.from_user.id)
        if (
            username != m.from_user.username
            or first_name != m.from_user.first_name
            or last_name != m.from_user.last_name
        ):
            await send_name_change_message(
                m.chat.id, m.from_user, username, first_name, last_name
            )


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
