from FallenRobot import pbot as pgram, BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

whisper_db = {}
switch_btn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("💒 Start Whispering", switch_inline_query_current_chat=".whisper")]]
)


@pgram.on_inline_query()
async def _whisper(_, inline_query):
    data = inline_query.query
    results = []

    if len(data.split()) < 3:
        mm = [
            InlineQueryResultArticle(
                title="Whisper",
                description=f"@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]",
                input_message_content=InputTextMessageContent(f"💒 Instructions:\n\n@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]"),
                thumb_url="https://graph.org/file/2c3c693d1b460c309da1d.jpg",
                reply_markup=switch_btn,
            )
        ]
    else:
        try:
            user_id = data.split()[1]
            msg = data.split(None, 2)[2]
        except IndexError:
            pass

        try:
            user = await _.get_users(user_id)
            whisper_btn = InlineKeyboardMarkup(
                [[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]]
            )
            mm = [
                InlineQueryResultArticle(
                    title="Whisper",
                    description=f"Start a whisper with {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"💒 Start a whisper with {user.first_name}.\n\nSend /s to send the message."),
                    thumb_url="https://graph.org/file/2c3c693d1b460c309da1d.jpg",
                    reply_markup=whisper_btn,
                )
            ]
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except Exception as e:
            print(e)
            mm = [
                InlineQueryResultArticle(
                    title="Whisper",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("Invalid username or ID!"),
                    thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg",
                    reply_markup=switch_btn,
                )
            ]

    results.append(mm)
    await inline_query.answer(results)


@pgram.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id

    if user_id not in [from_user, to_user]:
        return await query.answer("This whisper is not for you 🚧", show_alert=True)

    search_msg = f"{from_user}_{to_user}"
    try:
        msg = whisper_db[search_msg]
    except KeyError:
        msg = "🚫 Error‼️\n\nWhisper has been deleted from the database!"

    await query.answer(msg, show_alert=True)
