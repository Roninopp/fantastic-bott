import requests
from FallenRobot import pbot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# By @NandhaBots and @KishoreDxD on telegram

@app.on_message(filters.command("ud"))
async def urban(_, m):
    user_id = m.from_user.id
    if len(m.text.split()) == 1:
        return await m.reply("Enter the text for which you would like to find the definition.")
    text = m.text.split(None, 1)[1]
    api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
    mm = api["list"]
    if 0 == len(mm):
        reply_txt = "No results found! You can try searching on Google."
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Google it!", url=f"https://www.google.com/search?q={text}")]])
        return await m.reply_text(text=reply_txt, reply_markup=buttons, parse_mode="markdown")
    string = f"🔍 **Word**: {mm[0].get('word')}\n\n📝 **Definition**: {mm[0].get('definition').replace('[', '').replace(']', '')}\n\n✏️ **Example**: {mm[0].get('example').replace('[', '').replace(']', '')}"
    if 1 == len(mm):
        return await m.reply_text(text=string)
    else:
        num = 0
        return await m.reply_text(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Next', callback_data=f"udnxt:{user_id}:{text}:{num}")]]))

@app.on_callback_query(filters.regex("^udnxt"))
async def next(_, query):
    user_id = int(query.data.split(":")[1])
    text = str(query.data.split(":")[2])
    num = int(query.data.split(":")[3]) + 1
    if not query.from_user.id == user_id:
        return await query.answer("This is not for You!")
    api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
    mm = api["list"]
    uwu = mm[num]
    if num == len(mm) - 1:
        string = f"🔍 **Word**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition').replace('[', '').replace(']', '')}\n\n✏️ **Example**: {uwu.get('example').replace('[', '').replace(']', '')}\n\n"
        string += f"Page: {num + 1}/{len(mm)}"
        return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Back', callback_data=f"udbck:{query.from_user.id}:{text}:{num}")]]))
    else:
        string = f"🔍 **Word**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition').replace('[', '').replace(']', '')}\n\n✏️ **Example**: {uwu.get('example').replace('[', '').replace(']', '')}\n\n"
        string += f"Page: {num + 1}/{len(mm)}"
        buttons = [[
            InlineKeyboardButton("Back ⏮️", callback_data=f"udbck:{query.from_user.id}:{text}:{num}"),
            InlineKeyboardButton("Next ⏭️", callback_data=f"udnxt:{query.from_user.id}:{text}:{num}")
        ]]
        return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^udbck"))
async def back(_, query):
    user_id = int(query.data.split(":")[1])
    text = str(query.data.split(":")[2])
    num = int(query.data.split(":")[3]) - 1
    if not query.from_user.id == user_id:
        return await query.answer("This is not for You!")
    api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
    mm = api["list"]
    uwu = mm[num]
    if num == 0:
        string = f"🔍 **Word**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition').replace('[', '').replace(']', '')}\n\n✏️ **Example**: {uwu.get('example').replace('[', '').replace(']', '')}\n\n"
        string += f"Page: {num + 1}/{len(mm)}"
        return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Next', callback_data=f"udnxt:{query.from_user.id}:{text}:{num}")]]))
    else:
        string = f"🔍 **Word**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition').replace('[', '').replace(']', '')}\n\n✏️ **Example**: {uwu.get('example').replace('[', '').replace(']', '')}\n\n"
        string += f"Page: {num + 1}/{len(mm)}"
        buttons = [[
            InlineKeyboardButton("Back ⏮️", callback_data=f"udbck:{query.from_user.id}:{text}:{num}"),
            InlineKeyboardButton("Next ⏭️", callback_data=f"udnxt:{query.from_user.id}:{text}:{num}")
        ]]
        return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup(buttons))
            
