from FallenRobot.utils.mongo import db
from FallenRobot import pbot as pgram
from pyrogram import filters, Client ,errors, enums 
from FallenRobot.modules.pyrogram_funcs.status import user_admin,bot_admin
from pyrogram.raw.base import Update
from pyrogram.raw import types, functions
from FallenRobot.modules.mongo.antichannel_db import *


@pgram.on_message(filters.command("antichannelmode") & filters.group)
@user_admin
@bot_admin
async def _antichannelmode(_, message):
    chat_id = message.chat.id
    args = message.text.split()
    mm = await isModOn(chat_id)
    if len(args) < 2:
        return await message.reply_text('ᴜsᴀɢᴇ : /antichannelmode [ᴏɴ/ᴏғғ]')

    if "on" in args:
        if not mm:
            await antichannelmode_on(chat_id)
            return await message.reply_text("**ɴᴏᴡ ɪ ᴡɪʟʟ ʙᴀɴ ᴜsᴇʀs ᴡʜᴏ ᴄʜᴀᴛ ᴜsɪɴɢ ᴄʜᴀɴɴᴇʟs**")
        return await message.reply_text("**ᴀɴᴛɪᴄʜᴀɴɴᴇʟᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴʙᴀʟᴇᴅ**")
    elif "off" in args:
        if not mm:
            return await message.reply_text("**ᴀɴᴛɪᴄʜᴀɴɴᴇʟᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ**")
        await antichannelmode_off(chat_id)
        return await message.reply_text("**ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪᴄʜᴀɴɴᴇʟᴍᴏᴅᴇ**")

@pgram.on_message(filters.group,group=23)
async def _message_handler(client, message):
    if not (await isModOn(message.chat.id)):
        return
    chat_id = message.chat.id
    if message.sender_chat and message.sender_chat.type == enums.ChatType.CHANNEL and not message.chat.linked_chat:
        try:
            await message.delete()
            channel_id = message.sender_chat.id
            await client.invoke(functions.channels.EditBanned(
                    channel=await client.resolve_peer(chat_id),
                    participant=await client.resolve_peer(channel_id),
                    banned_rights=types.ChatBannedRights(
                        until_date=0,
                        view_messages=True,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_polls=True)))
        except Exception as e:
            print(e)
