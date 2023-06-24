from pyrogram import filters,enums
from FallenRobot import pbot as pgram
from FallenRobot import DRAGONS as SUPREME_USERS
from FallenRobot.modules.pyrogram_funcs.status import user_admin
from FallenRobot.modules.pyrogram_funcs.extracting_id import extract_user_id
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from FallenRobot.modules.mongo.approve_db import *
from .pyrogram_funcs.decorators import control_user,command

SPAM_CHATS = []

@pgram.on_message(filters.command("approve"))
@control_user()
@user_admin
async def _approve(_, message):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text("**ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ.**")
    
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        return await message.reply_text("**ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴ - ʙʟᴏᴄᴋʟɪsᴛs,ᴀɴᴛɪғʟᴏᴏᴅ,etc ᴀʟʀᴇᴀᴅʏ ᴅᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ.**")       
    check_user = await is_approved(chat_id,user_id)
    if check_user:
        return await message.reply_text(f"{member.user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ")
    await approve_user(chat_id, user_id)
    return await message.reply_text(f"{member.user.mention} ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {message.chat.title}! ᴛʜᴇʏ ᴡɪʟʟ ɴᴏᴡ ʙᴇ ɪɢɴᴏʀᴇᴅ ʙʏ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴀᴅᴍɪɴ ᴀᴄᴛɪᴏɴs ʟɪᴋᴇ ʙʟᴏᴄᴋʟɪsᴛs, ᴀɴᴅ ᴀɴᴛɪғʟᴏᴏᴅ.")              


@pgram.on_message(filters.command("disapprove"))
@control_user()
@user_admin
async def _approve(_, message):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text("**ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ.**")
    
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        return await message.reply_text("**ᴛʜɪs ᴜsᴇʀ ɪs ᴀɴ ᴀᴅᴍɪɴ, ᴛʜᴇʏ ᴄᴀɴ'ᴛ ʙᴇ ᴜɴᴀᴘᴘʀᴏᴠᴇᴅ**")       
    check_user = await is_approved(chat_id,user_id)
    if not check_user:
        return await message.reply_text(f"{member.user.mention} ɪsɴ'ᴛ ᴀᴘᴘʀᴏᴠᴇᴅ ʏᴇᴛ!")
    await disapprove_user(chat_id, user_id)
    await message.reply_text(f"{member.user.mention} ɪs ɴᴏ ʟᴏɴɢᴇʀ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {message.chat.title}")              

@pgram.on_message(filters.command("approved"))
@control_user()
@user_admin
async def _approvedlist(_, message):
    chat_id = message.chat.id
    list1 = await approved_users(chat_id)
    if not list:
        return await message.reply_text("**ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
    text = "❗ʟɪsᴛ ᴏғ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.\n"
    for i in list1:
        try:
            member = await _.get_chat_member(chat_id,int(i))
            text += f"⦾ {member.user.mention}\n"
        except:
            pass
    await message.reply_text(text)   

@pgram.on_message(filters.command("approval"))
@control_user()
@user_admin
async def _approval(_, message):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)    
    if not user_id:
        return await message.reply_text("**ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ!**")
    try :
        m = await _.get_chat_member(chat_id,user_id)
    except Exception as e:
        print(e)
        return await message.reply_text("**ᴜsᴇʀ ɪsɴ'ᴛ ʜᴇʀᴇ**")
    check_user = await is_approved(chat_id,user_id)
    if check_user:
        return await message.reply_text(f"{m.user.mention} ɪs ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀ. Lᴏᴄᴋs, ᴀɴᴛɪғʟᴏᴏᴅ, ᴀɴᴅ ʙʟᴏᴄᴋʟɪsᴛs ᴡᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ")
    
    return await message.reply_text(f"{m.user.mention} ɪs ɴᴏᴛ ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀ. ᴛʜᴇʏ ᴀʀᴇ ᴀғғᴇᴄᴛᴇᴅ ʙʏ ɴᴏʀᴍᴀʟ ᴄᴏᴍᴍᴀɴᴅs") 

@pgram.on_message(filters.command("disapproveall") & filters.group)
@control_user()
async def _disappall(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    owner = await _.get_chat_member(chat_id, user_id)  # Retrieve group owner info
    if owner.status != enums.ChatMemberStatus.CREATOR:  # Check if the status is CREATOR
        return await message.reply_text("**ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ ᴄᴀɴ ᴅɪsᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ**")
    list1 = await approved_users(chat_id)
    if list1 is None:
        return await message.reply_text("**ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴜsᴇʀs", callback_data="unaproveall")],
         [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="admin_close")]]
    )
    await message.reply_text(
        "ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ ? "
        "ᴛʜɪs ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.", reply_markup=btn
    )

@pgram.on_callback_query(filters.regex("unaproveall"))
@control_user()
async def _unappall(_, query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    owner = await _.get_chat_member(chat_id, user_id)  # Retrieve group owner info
    if owner.status != enums.ChatMemberStatus.CREATOR or user_id not in SUPREME_USERS:
        return await query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ ᴄᴀɴ ᴅɪsᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ", show_alert=True)
    list1 = await approved_users(chat_id)
    SPAM_CHATS.append(chat_id)
    await query.message.edit_text(
        "sᴛᴀʀᴛᴇᴅ ᴅɪsᴀᴘᴘʀᴏᴠɪɴɢ ᴀʟʟ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ. ᴜsᴇ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss."
    )
    for user in list1:
        if chat_id not in SPAM_CHATS:
            break
        await disapprove_user(chat_id, int(user))
    await query.message.edit_text("**ᴅɪsᴀᴘᴘʀᴏᴠᴇᴅ ᴀʟʟ ᴜsᴇʀs**")
