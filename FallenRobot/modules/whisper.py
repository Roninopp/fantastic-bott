from FallenRobot import pbot as pgram, BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat="w")]])

@pgram.on_message(filters.command("whisper"))
async def _whisper(_, message):
    await message.reply_photo(
        photo="https://graph.org/file/33b3ac5d2fe66ec747971.jpg",
        caption="🫧 Click the button below to send a whisper to someone.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Send a Whisper", switch_inline_query_current_chat="")]]))


ALPHA = {}
BUN = None
SWITCH_PM = InlineKeyboardMarkup([[InlineKeyboardButton("📬 Send Whisper", switch_inline_query="")]])
HLP = "**🫧 Whisper Bot Help**\n\n» `@{} [username] [whisper]`\n\nEx: `@{} @HSSLevii hello‼️`"
res1 = [InlineQueryResultArticle(title="Whisper", description="Invalid username or ID!",
                                 input_message_content=InputTextMessageContent("Invalid username or ID!"),
                                 thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg")]


@pgram.on_inline_query()
async def inline(app, query):
    global ALPHA, BUN
    if not BUN:
        BUN = (await app.get_me()).username
    res = [InlineQueryResultArticle(title="Whisper",
                                    description=f"@{BUN} [USERNAME | ID] [TEXT]",
                                    input_message_content=InputTextMessageContent(f"📬 Usage:\n\n@{BUN} username text."),
                                    thumb_url="https://graph.org/file/4d5d893c631e83c590a75.jpg")]
    txt = query.query
    if not len(txt.split(None, 1)) == 2:
        await app.answer_inline_query(query.id, results=res, cache_time=0)
    try:
        tar = int(txt.split()[0])
    except:
        try:
            tar = (await app.get_users(txt.split()[0])).id
        except:
            await app.answer_inline_query(query.id, results=res1, cache_time=0)
    try:
        Na = (await app.get_users(tar)).first_name
    except:
        pass
    try:
        whisp = txt.split(None, 1)[1]
    except IndexError:
        pass
    try:
        WTXT = "💌 A whisper has been sent to {}.\n\nOnly he/she can open it."
        SHOW = InlineKeyboardMarkup([[InlineKeyboardButton("📬 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
        SHOW_ONE = InlineKeyboardMarkup([[InlineKeyboardButton("⏲️ One-Time Whisper",
                                                               callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
        res2 = [InlineQueryResultArticle(title="Whisper",
                                         description=f"Send a Whisper to {Na}!",
                                         input_message_content=InputTextMessageContent(WTXT.format(Na)),
                                         thumb_url="https://graph.org/file/4d5d893c631e83c590a75.jpg",
                                         reply_markup=SHOW),
                InlineQueryResultArticle(title="Whisper",
                                         description=f"Send One-Time whisper to {Na}!",
                                         input_message_content=InputTextMessageContent(WTXT.format(Na)),
                                         thumb_url="https://graph.org/file/4d5d893c631e83c590a75.jpg",
                                         reply_markup=SHOW_ONE)]
        await app.answer_inline_query(query.id, results=res2, cache_time=0)
    except:
        pass
    try:
        ALPHA.pop(f"{query.from_user.id}_{tar}")
    except:
        pass
    try:
        ALPHA[f"{query.from_user.id}_{tar}"] = whisp
    except:
        pass


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
        msg = ALPHA[search_msg]
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
            input_message_content=InputTextMessageContent("Inline Commands"),
            thumb_url="https://graph.org/file/33b3ac5d2fe66ec747971.jpg",
            reply_markup=keywords
        )
    ]
    return answers


@pgram.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()
    
    if string.strip() == "":
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers)
    elif string.split()[0] == "w":
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)
      
