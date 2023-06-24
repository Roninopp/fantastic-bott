from pyrogram import filters,enums
from pyrogram.types import Message, CallbackQuery
from FallenRobot import pbot as pgram
from FallenRobot import DRAGONS as SUPREME_USERS
from pyrogram.enums import ChatMemberStatus
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

@pgram.on_message(filters.command("unapproveall") & filters.group)
@control_user()
async def unapproveall_users(_, m: Message):
    chat_id = m.chat.id

    all_approved = await approved_users(chat_id)
    if not all_approved:
        await m.reply_text("No one is approved in this chat.")
        return

    await m.reply_text(
        "Are you sure you want to remove everyone who is approved in this chat?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("UNAPPROVE ALL USERS", callback_data="unapprove_all")],
            [InlineKeyboardButton("❌ CLOSE", callback_data="admin_close")]
        ])
    )
    return

@pgram.on_callback_query(filters.regex("^unapprove_all$"))
async def unapproveall_callback(_, q: CallbackQuery):
    user_id = q.from_user.id
    chat_id = q.message.chat.id
    approved_people = await approved_users(chat_id)
    user_status = (await q.message.chat.get_member(user_id)).status
    if user_status != ChatMemberStatus.OWNER:
        await q.answer(
            "You're not even the group owner, don't try this explosive shit!",
            show_alert=True,
        )
        return
    await approvedb.delete_one({"chat_id": chat_id})
    for user_id in approved_people:
        await q.message.chat.restrict_member(
            user_id=user_id,
            permissions=q.message.chat.permissions,
        )
    await q.message.delete()
    await q.answer("Disapproved all users!", show_alert=True)
    return
