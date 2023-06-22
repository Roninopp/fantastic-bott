from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from FallenRobot import pbot as pgram
from pyrogram.errors import Unauthorized


@pgram.on_message(filters.command("whisper"))
async def _whisper(_, message):
    await message.reply_photo(
        photo="https://graph.org/file/33b3ac5d2fe66ec747971.jpg",
        caption="🫧 Click the button below to send a whisper to someone.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Send a Whisper", switch_inline_query_current_chat="")]]))


ALPHA = {}
BUN = None
SWITCH_PM = InlineKeyboardMarkup([[InlineKeyboardButton("📬 Send Whisper", switch_inline_query="")]])
HLP = "**🫧 Whisper Bot Help**\n\n» `@{} [username] [whisper]`\n\nEx: `@{} @HSSLevii Hello‼️`"
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
                                    input_message_content=InputTextMessageContent(f"**📍Usage:**\n\n@{BUN} @Yorr_Forgerr_Bot (Target Username or ID) (Your Message).\nExample: `@Yorr_Forgerr_Bot @username Yo, I Wanna Phuck You`"),
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
        SHOW = InlineKeyboardMarkup([[InlineKeyboardButton("📬 Whisper", callback_data=f"{query.from_user.id}_{tar}")]])
        SHOW_ONE = InlineKeyboardMarkup([[InlineKeyboardButton("🔩 One-Time Whisper",
                                                               callback_data=f"{query.from_user.id}_{tar}_one")]])
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


@pgram.on_callback_query()
async def cbq(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])       
    user_id = query.from_user.id
    if user_id not in [from_user, to_user]:
        return
    search_msg = f"{from_user}_{to_user}"
    try:
        msg = ALPHA[search_msg]
    except:
        msg = "🚫 Error‼️\n\nWhisper has been deleted from the database!"
    await query.answer(msg, show_alert=True)
    
