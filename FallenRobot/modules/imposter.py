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

@app.on_message(filters.group & filters.command("history") & ~filters.bot & ~filters.via_bot)
async def search_history(_, m):
    if len(m.command) == 1:
        # Check if the command was replied to a message
        if m.reply_to_message and m.reply_to_message.from_user:
            user_id = m.reply_to_message.from_user.id
            username = m.reply_to_message.from_user.username
        else:
            return await kirimPesan(m, f"Please provide a user ID, username, or reply to a message to search the history.")
    else:
        query = m.command[1].strip()
        user_id = None
        if query.startswith("@"):
            username = query[1:]
            try:
                user = await app.get_users(username)
                user_id = user.id
            except:
                await kirimPesan(m, f"User with username '{username}' not found.")
        else:
            try:
                user_id = int(query)
            except ValueError:
                await kirimPesan(m, f"Invalid user ID or username. Please provide a valid user ID or username to search the history.")

    if user_id is not None:
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

            # Interactive Name History
            if len(name_history) > 0:
                await app.send_message(
                    chat_id=m.chat.id,
                    text="To view the complete name change history, use the buttons below:",
                    reply_markup={
                        "inline_keyboard": [
                            [
                                {
                                    "text": "View All",
                                    "callback_data": f"view_name_history:{user_id}:1"
                                }
                            ]
                        ]
                    }
                )
        else:
            await kirimPesan(m, "User data not found.")

@app.on_callback_query(filters.regex(r"^view_name_history:(\d+):(\d+)$"))
async def callback_view_name_history(_, cq):
    user_id = int(cq.matches[0].group(1))
    page_number = int(cq.matches[0].group(2))

    name_history = await history_db.find({"user_id": user_id}).sort("_id", -1).skip((page_number - 1) * 5).limit(5).to_list(None)
    
    history_msg = "<b>🔰 Name History:</b>\n\n"
    history_msg += f"<code>👤 {user_id}</code>\n\n"

    for i, history in enumerate(name_history, start=(page_number - 1) * 5 + 1):
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

    if len(name_history) == 5:
        history_msg += "<i>More name changes available. Use the buttons below to navigate:</i>"

        inline_keyboard = []
        if page_number > 1:
            inline_keyboard.append(
                {
                    "text": "Previous",
                    "callback_data": f"view_name_history:{user_id}:{page_number - 1}"
                }
            )
        inline_keyboard.append(
            {
                "text": "Next",
                "callback_data": f"view_name_history:{user_id}:{page_number + 1}"
            }
        )

        await cq.message.edit_text(history_msg, reply_markup={"inline_keyboard": [inline_keyboard]})
    else:
        await cq.message.edit_text(history_msg)

@app.on_message(filters.group & filters.command("namechangelog") & ~filters.bot & ~filters.via_bot)
@adminsOnly("can_change_info")
async def name_change_log(_, m):
    if len(m.command) == 1:
        return await kirimPesan(m, f"Please provide the user ID or username to get the name change log.")
    
    query = m.command[1].strip()
    user_id = None
    if query.startswith("@"):
        username = query[1:]
        try:
            user = await app.get_users(username)
            user_id = user.id
        except:
            await kirimPesan(m, f"User with username '{username}' not found.")
    else:
        try:
            user_id = int(query)
        except ValueError:
            await kirimPesan(m, f"Invalid user ID or username. Please provide a valid user ID or username to get the name change log.")

    if user_id is not None:
        if await cek_userdata(user_id):
            username, first_name, last_name = await get_userdata(user_id)
            log_msg = "<b>📜 Name Change Log:</b>\n\n"
            log_msg += f"<code>👤 {user_id}</code>\n\n"

            name_changes = await history_db.find({"user_id": user_id}).sort("_id", -1).to_list(None)

            for i, change in enumerate(name_changes, start=1):
                timestamp = change["_id"].generation_time.astimezone(pytz.timezone("Asia/Kolkata"))
                formatted_timestamp = timestamp.strftime("[<code>%d/%m/%Y %I:%M:%S %p</code>]")
                log_msg += f"<code>{i}.</code> {formatted_timestamp}\n"
                log_msg += f"   <code>From:</code> {escape(change['old_first_name'])} <code>{escape(change['old_last_name']) if change['old_last_name'] else ''}</code>\n"
                log_msg += f"   <code>To:</code> {escape(change['new_first_name'])} <code>{escape(change['new_last_name']) if change['new_last_name'] else ''}</code>\n"
                log_msg += "\n"

            await kirimPesan(m, log_msg, quote=True)
        else:
            await kirimPesan(m, "User data not found.")

__mod_name__ = "ɪᴍᴘᴏsᴛᴇʀ ᴅᴇᴛᴇᴄᴛɪᴏɴ"
__help__ = """
*• /detectimposter:* Use this command to track name and username changes in the group. If a user changes their name and username, the bot will send a message showing any related changes.

*• /history:* Reply to a user with this command to get their previous name change history.

*• /namechangelog:* Get the name change log for a specific user by providing their user ID or username.
"""
                         
