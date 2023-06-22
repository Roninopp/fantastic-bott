from FallenRobot import pbot as pgram, BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []
    
    if len(data.split()) < 3:
        mm = [
            InlineQueryResultArticle(
                title="💒 Whisper",
                description=f"@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]",
                input_message_content=InputTextMessageContent(f"💒 Usage:\n\n@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]"),
                thumb_url="https://graph.org/file/2c3c693d1b460c309da1d.jpg",
                reply_markup=switch_btn
            )
        ]
    else:
        try:
            user_id = data.split()[1]
            msg = data.split(None, 2)[2]
        except IndexError as e:
            pass
        
        try:
            user = await _.get_users(user_id)
        except:
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("Invalid username or ID!"),
                    thumb_url="https://graph.org/file/4d5d893c631e83c590a75.jpg",
                    reply_markup=switch_btn
                )
            ]
        
        try:
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⏲️ One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description=f"Send a Whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"💒 You are sending a whisper to {user.first_name}.\n\nType your message/sentence."),
                    thumb_url="https://graph.org/file/4d5d893c631e83c590a75.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="⏲️ One-Time Whisper",
                    description=f"Send a one-time whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"⏲️ You are sending a one-time whisper to {user.first_name}.\n\nType your message/sentence."),
                    thumb_url="https://graph.org/file/4d5d893c631e83c590a75.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
        except:
            pass
        
        try:
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except:
            pass
    
    results.append(mm)
    return results


@pgram.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
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


keywords = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Send Whisper", switch_inline_query_current_chat="w")]])

async def in_help():
    answers = [
        InlineQueryResultArticle(
            title="Help Menu!",
            input_message_content=InputTextMessageContent("Inline Commands!"),
            thumb_url="https://graph.org/file/33b3ac5d2fe66ec747971.jpg",
            reply_markup=keywords
        )
    ]
    return answers


@pgram.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()
    
    if string.strip() == "":
        answers = await _whisper()
        await inline_query.answer(answers)
    elif string.split()[0] == "w":
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)
      
