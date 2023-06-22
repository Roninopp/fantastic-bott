from FallenRobot import pbot as pgram, BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat=".whisper")]])

async def process_message(_, message):
    if message.reply_to_message:
        replied_msg = message.reply_to_message
        if replied_msg.from_user and replied_msg.from_user.id != _.me.id:
            sender = replied_msg.from_user
            text = message.text
            if not text:
                await message.reply("Please provide a whisper message.")
                return
            whisper_db[f"{message.from_user.id}_{sender.id}"] = text
            await message.reply(f"Whisper sent to {sender.mention()} successfully!")
        else:
            await message.reply("Please reply to a message from the user you want to whisper to.")
    else:
        await message.reply("Please reply to a message from the user you want to whisper to.")


async def _whisper(_, inline_query):
    data = inline_query.query
    results = []
    
    if len(data.split()) < 2:
        mm = [
            InlineQueryResultArticle(
                title="💒 Whisper",
                description=f"@{BOT_USERNAME} [USERNAME | ID]",
                input_message_content=InputTextMessageContent(f"💒 Usage:\n\n@{BOT_USERNAME} [USERNAME | ID]"),
                thumb_url="https://graph.org/file/2c3c693d1b460c309da1d.jpg"
            )
        ]
    else:
        try:
            user_id = data.split()[1]
        except IndexError:
            pass
        
        try:
            user = await _.get_users(user_id)
        except:
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("Invalid username or ID!"),
                    thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg"
                )
            ]
        
        try:
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⏲️ One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description=f"Send a Whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"💒 You are sending a whisper to {user.first_name}.\n\nType your message/sentence.")
                ),
                InlineQueryResultArticle(
                    title="⏲️ One-Time Whisper",
                    description=f"Send a one-time whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"⏲️ You are sending a one-time whisper to {user.first_name}.\n\nType your message/sentence.")
                )
            ]
        except Exception as e:
            print(e)
    
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


@pgram.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()
    
    if BOT_USERNAME in string:
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)


# Add filters to process the messages
@pgram.on_message(filters.text & ~filters.edited & filters.private)
async def process_private_message(_, message):
    await process_message(_, message)


@pgram.on_message(filters.text & ~filters.edited & filters.group)
async def process_group_message(_, message):
    if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == _.me.id:
        await process_message(_, message)
