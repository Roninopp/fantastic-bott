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


def format_timestamp(timestamp):
    formatted_timestamp = timestamp.strftime("[%d/%m/%Y %I:%M:%S %p]")
    return f"<code>{formatted_timestamp}</code>"


def format_name_change(change_first_name, change_last_name):
    formatted_first_name = f"<code>{escape(change_first_name)}</code>"
    formatted_last_name = f"<code>{escape(change_last_name)}</code>" if change_last_name else "None"
    return f"{formatted_first_name} {formatted_last_name}"


def format_username_change(change_username):
    if change_username:
        formatted_username = escape(change_username)
        return f"@{formatted_username}"
    return ""


async def get_user_data(user_id):
    username, first_name, last_name = await get_userdata(user_id)
    return username, first_name, last_name


def get_user_history(user_id):
    name_history = list(history_db.find({"user_id": user_id}).sort("_id", -1))
    return name_history


def get_user_history_message(user_id):
    username, first_name, last_name = await get_user_data(user_id)
    history_msg = "<b>🔰 Name History:</b>\n\n"
    history_msg += f"<code>👤 {user_id}</code>\n\n"

    name_history = get_user_history(user_id)

    for i, history in enumerate(name_history[::-1], start=1):
        timestamp = history["_id"].generation_time.astimezone(pytz.timezone("Asia/Kolkata"))
        formatted_timestamp = format_timestamp(timestamp)
        change_first_name = history["first_name"]
        change_last_name = history["last_name"]
        change_username = history["username"]

        history_msg += f"<code>{i}. {formatted_timestamp}</code>\n"
        history_msg += f"   {format_name_change(change_first_name, change_last_name)}\n"
        history_msg += f"   {format_username_change(change_username)}\n\n"

    return history_msg


@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=3)
async def cek_mataa(_, m):
    if not await is_sangmata_on(m.chat.id):
        return
    if not await cek_userdata(m.from_user.id):
        await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
    else:
        if m.text and m.text.startswith("/history"):
            command_args = m.text.split()[1:]
            if command_args:
                search_query = command_args[0]
                user_id = None
                if search_query.isdigit():
                    user_id = int(search_query)
                else:
                    user = await app.get_users(search_query)
                    if user:
                        user_id = user.id

                if user_id:
                    username, first_name, last_name = await get_user_data(user_id)
                    history_msg = await get_user_history_message(user_id, username, first_name, last_name)
                    await kirimPesan(m, history_msg, quote=True)
                    return
            else:
                user_id = m.reply_to_message.from_user.id if m.reply_to_message else m.from_user.id
                username, first_name, last_name = await get_user_data(user_id)
                history_msg = await get_user_history_message(user_id, username, first_name, last_name)
                await kirimPesan(m, history_msg, quote=True)


@app.on_message(filters.group & filters.reply & filters.command("history"))
async def cek_mataa_reply(_, m):
    if not await is_sangmata_on(m.chat.id):
        return
    if not await cek_userdata(m.from_user.id):
        await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
    else:
        user_id = m.reply_to_message.from_user.id
        history_msg = get_user_history_message(user_id)
        await kirimPesan(m, history_msg, quote=True)


@app.on_message(filters.group & filters.command("history") & filters.regex("^/history@"))
async def cek_mataa_username(_, m):
    if not await is_sangmata_on(m.chat.id):
        return
    if not await cek_userdata(m.from_user.id):
        await add_userdata(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
    else:
        command_args = m.text.split()[1:]
        if command_args:
            search_query = command_args[0]
            user = await app.get_users(search_query)
            if user:
                user_id = user.id
                history_msg = get_user_history_message(user_id)
                await kirimPesan(m, history_msg, quote=True)
        
