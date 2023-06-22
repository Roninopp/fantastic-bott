from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from FallenRobot import pbot as pgram
from pyrogram.errors import Unauthorized
from pymongo import MongoClient

# Establish MongoDB connection
client = MongoClient("mongodb+srv://eren:eren@cluster0.yxuwg4r.mongodb.net/?retryWrites=true&w=majority")
db = client["your_database_name"]
whisper_collection = db["whisper_messages"]


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
async def cbq(app, iquery):
    try:
        id = iquery.from_user.id
        stark = iquery.data.split("_")
        if id not in [int(stark[0]), int(stark[1]), 5667156680]:
            try:
                await app.send_message(stark[0], f"{iquery.from_user.mention} is trying to open your whisper.")
            except Unauthorized:
                pass
            return await iquery.answer("This whisper is not for you 🚧", show_alert=True)
        for_search = stark[0] + "_" + stark[1]
        print(stark)
        try:
            msg = ALPHA[for_search]
        except:
            msg = "🚫 Error‼️\n\nWhisper has been deleted from the database!"

        # Store whisper message in the database
        whisper_data = {
            "sender_id": int(stark[0]),
            "receiver_id": int(stark[1]),
            "message": msg
        }
        whisper_collection.insert_one(whisper_data)

        SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline 🪝", switch_inline_query_current_chat="")]])
        await iquery.answer(msg, show_alert=True)
        if stark[2] == "one":
            if id == int(stark[1]):
                await iquery.edit_message_text(
                    "📬 Whisper has been read!\n\nPress the button below to send whisper!", reply_markup=SWITCH)
    except Exception as e:
        await iquery.answer(str(e), show_alert=True)
