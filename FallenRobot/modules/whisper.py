from FallenRobot import pbot as pgram, BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat=".whisper")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []
    
    if BOT_USERNAME in data:
        # Extract the username mentioned in the query
        username = data.split(BOT_USERNAME)[1].strip()
        
        if username:
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{username}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⏲️ One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{username}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description=f"Send a Whisper to {username}!",
                    input_message_content=InputTextMessageContent(f"💒 You are sending a whisper to {username}.\n\nType your message/sentence."),
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="⏲️ One-Time Whisper",
                    description=f"Send a one-time whisper to {username}!",
                    input_message_content=InputTextMessageContent(f"⏲️ You are sending a one-time whisper to {username}.\n\nType your message/sentence."),
                    reply_markup=one_time_whisper_btn
                )
            ]
            results.append(mm)
    
    return results


@pgram.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = data[2]
    user_id = query.from_user.id
    
    if user_id not in [from_user, to_user]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} is trying to open your whisper.")
        except Unauthorized:
            pass
        
        return await query.answer("This whisper is not for you 🚧", show_alert=True)
    
    search_msg = f"{from_user}_{to_user}"
    
    try:
        msg = whisper_db[search_msg]
    except:
        msg = "🚫 Error!\n\nWhisper has been deleted from the database!"
    
    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline 🪝", switch_inline_query_current_chat="")]])
    
    await query.answer(msg, show_alert=True)
    
    if data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text("📬 Whisper has been read!\n\nPress the button below to send a whisper!", reply_markup=SWITCH)


@pgram.on_inline_query()
async def bot_inline(_, inline_query):
    results = await _whisper(_, inline_query)
    await inline_query.answer(results, cache_time=0)
    
