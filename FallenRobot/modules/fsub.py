from FallenRobot import pbot as pgram,BOT_ID
from FallenRobot import DRAGONS as CHAD
from pyrogram import filters, enums 
from FallenRobot.modules.pyrogram_funcs.status import (
    user_admin,
    bot_admin,
    bot_can_ban )
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , CallbackQuery ,ChatPermissions
from pyrogram.errors import BadRequest 
from FallenRobot.modules.mongo.approve_db import approved_users
from FallenRobot.modules.mongo.fsub_db import *

forsesub_watcher = 6

@pgram.on_message(filters.command("fsub") & filters.group)
@user_admin
@bot_admin
@bot_can_ban
async def _force_sub(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    args = message.text.split()
    user = await _.get_chat_member(chat_id,user_id)
    if not user.status == ChatMemberStatus.OWNER :
        return await message.reply_text("ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ ʀᴇǫᴜɪʀᴇᴅ \nʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ʙᴇ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ.")           
    if "OFF".lower() in args:
         await fsub_off(chat_id)
         return await message.reply_text("**❌ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɪs ᴅɪsᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ**")
    elif len(args) < 2:
        return await message.reply_text("ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ ᴛᴏ ᴇɴᴀʙʟᴇ ғᴏʀᴄᴇ sᴜʙ")
    ch = args[1]
    try:
        channel = await _.get_chat(ch)
    except:
        return await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ᴜsᴇʀɴᴀᴍᴇ ᴘʀᴏᴠɪᴅᴇᴅ")
    try:
        await _.get_chat_member(channel.id,BOT_ID)
    except BadRequest :
        return await message.reply_text("ɪ ᴀᴍ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ. ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ sᴜʀᴇ ᴀᴍ ᴀᴅᴍɪɴ ᴛʜᴇʀᴇ.")
    member = await _.get_chat_member(channel.id,BOT_ID)
    if member.status != ChatMemberStatus.ADMINISTRATOR:
        return await message.reply_text(
                f"❗**ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ**\nI ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ [ᴄʜᴀɴɴᴇʟ](https://t.me/{ch}). ᴀᴅᴅ ᴍᴇ ᴀs ᴀ ᴀᴅᴍɪɴ ɪɴ ᴏʀᴅᴇʀ ᴛᴏ ᴇɴᴀʙʟᴇ ғᴏʀᴄᴇsᴜʙsᴄʀɪʙᴇ.")

    await fsub_on(chat_id,channel.id)
    await message.reply_text(f"✅ **ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɪs ᴇɴᴀʙʟᴇᴅ** to @{channel.username}.")

@pgram.on_message(filters.command("fsub_stats") & filters.group)
@user_admin
async def _force_stat(_, message):
    chat_id = message.chat.id
    status = await fsub_stat(chat_id)
    if status is True:
        channel = await _.get_chat(await get_channel(chat_id)) 
        return await message.reply_text(f"ғᴏʀᴄᴇsᴜʙ ɪs ᴇɴᴀʙʟᴇᴅ ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ ᴍᴜᴛɪɴɢ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇɴ'ᴛ ɪᴏɪɴᴇᴅ [ᴛʜɪs ᴄʜᴀɴɴᴇʟ](t.me/{channel.username})")
    return await message.reply_text("ғᴏʀᴄᴇ sᴜʙ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ")

@pgram.on_message(group=forsesub_watcher)
async def _mute(_, message):
    chat_id = message.chat.id
    if not await fsub_stat(chat_id):
        return
    if not message.from_user:
        return
    SUPREME = await approved_users(chat_id) + CHAD    
    async for m in _.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        SUPREME.append(m.user.id)
    if message.from_user.id in SUPREME:
        return 
    ch = await get_channel(chat_id)
    channel = await _.get_chat(ch)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",url=f"t.me/{channel.username}"), InlineKeyboardButton("🤐 ᴜɴᴍᴜᴛᴇ ᴍᴇ", callback_data=f"fsubuser_{message.from_user.id}")]])
    msg = f"{message.from_user.mention}, ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ [ᴄʜᴀɴɴᴇʟ](t.me/{channel.username}) ʏᴇᴛ❗ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ᴘʀᴇss ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴜɴᴍᴜᴛᴇ ʏᴏᴜʀsᴇʟғ"
    await message.reply_text(msg,reply_markup=buttons)
    try:
        await _.restrict_chat_member(chat_id, message.from_user.id, ChatPermissions(can_send_messages=False))
    except Exception as e:
        await message.reply_text(e)
  
@pgram.on_callback_query(filters.regex(pattern=r"fsubuser_(.*)"))
async def ok(_, query : CallbackQuery):
    muted_user = int(query.data.split("_")[1])
    chat_id = query.message.chat.id
    ch = await get_channel(chat_id)
    members = []
    async for member in _.get_chat_members(ch):
        members.append(member.user.id)
    user_id = query.from_user.id
    if user_id != muted_user:
        await _.answer_callback_query(query.id,text="❌ ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ.",show_alert=True)
        return   
              
    if not muted_user in members:
        return await _.answer_callback_query(query.id,text="ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ғɪʀsᴛ, ᴛᴏ ɢᴇᴛ ᴜɴᴍᴜᴛᴇᴅ!",show_alert=True)
    
    try :
        await _.unban_chat_member(chat_id,muted_user)
    except Exception as er:
        print(er)
    await query.message.delete()
