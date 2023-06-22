from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup,InlineQueryResultArticle,InputTextMessageContent
from FallenRobot import pbot as pgram 
from pyrogram.errors import Unauthorized 


@pgram.on_message(filters.command("whisper"))
async def _whisper(_, message):
    await message.reply_photo(
    photo="https://graph.org/file/2c3c693d1b460c309da1d.jpg",
    caption="⚗️ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴇɴᴅ ᴀ ᴡʜɪsᴘᴇʀ ᴛᴏ sᴏᴍᴇᴏɴᴇ.",
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💌 sᴇɴᴅ ᴀ ᴡʜɪsᴘᴇʀ",switch_inline_query_current_chat="")]]))

ALPHA = {}
BUN = None
SWITCH_PM = InlineKeyboardMarkup([[InlineKeyboardButton("💌 sᴇɴᴅ ᴡʜɪsᴘᴇʀ", switch_inline_query="")]])
HLP = "**🧪 ᴡʜɪsᴘᴇʀ ʙᴏᴛ ʜᴇʟᴘ**\n\n» `@{} [ᴜsᴇʀɴᴀᴍᴇ] [ᴡʜɪsᴘᴇʀ]`\n\nEx : `@{} @NoobStark_21 ʜᴇʟʟᴏ ‼️`"
res1 = [InlineQueryResultArticle(title="ᴡʜɪsᴘᴇʀ", description="Iɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ Iᴅ !", input_message_content=InputTextMessageContent("Iɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ Iᴅ !"),thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg")]

@pgram.on_inline_query()
async def inline(app, query):
    global ALPHA, BUN
    if not BUN:
        BUN = (await app.get_me()).username
    res = [InlineQueryResultArticle(title="ᴡʜɪsᴘᴇʀ", description=f"@{BUN} [ USERNAME | ID ] [ TEXT ]", input_message_content=InputTextMessageContent(f"💌 ᴜsᴀɢᴇ :\ɴ\ɴ@{BUN} ᴜsᴇʀɴᴀᴍᴇ ᴛᴇxᴛ."), thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg")]
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
        WTXT = "💌 A ᴡʜɪsᴘᴇʀ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ {}.\n\nᴏɴʟʏ ʜᴇ / sʜᴇ ᴄᴀɴ ᴏᴘᴇɴ ɪᴛ."
        SHOW = InlineKeyboardMarkup([[InlineKeyboardButton("💌 ᴡʜɪsᴘᴇʀ", callback_data=f"{query.from_user.id}_{tar}")]])
        SHOW_ONE = InlineKeyboardMarkup([[InlineKeyboardButton("⏲️ ᴏɴᴇ ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ", callback_data=f"{query.from_user.id}_{tar}_one")]])
        res2 = [InlineQueryResultArticle(title="ᴡʜɪsᴘᴇʀ", description=f"sᴇɴᴅ ᴀ ᴡʜɪsᴘᴇʀ ᴛᴏ {Na} !", input_message_content=InputTextMessageContent(WTXT.format(Na)),thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg", reply_markup=SHOW), InlineQueryResultArticle(title="ᴡʜɪsᴘᴇʀ", description=f"sᴇɴᴅ ᴏɴᴇ ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ ᴛᴏ {Na} !", input_message_content=InputTextMessageContent(WTXT.format(Na)),thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg", reply_markup=SHOW_ONE)]
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
        if id not in [int(stark[0]),int(stark[1]),5285561060]:
            try:
                  await app.send_message(stark[0],f"{iquery.from_user.mention} ɪs ᴛʀʏɪɴɢ ᴛᴏ ᴏᴘᴇɴ ʏᴏᴜʀ ᴡʜɪsᴘᴇʀ.")
            except Unauthorized:
                 pass         
            return await iquery.answer("ᴛʜɪs ᴡʜɪsᴘᴇʀ ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ 🚧", show_alert=True)        
        for_search = stark[0] + "_" + stark[1]
        print(stark)
        try:
            msg = ALPHA[for_search] 
        except:
            msg = "🚫 ᴇʀʀᴏʀ ‼️\n\nᴡʜɪsᴘᴇʀ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ !"
        SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("ɢᴏ ɪɴʟɪɴᴇ ☁️", switch_inline_query_current_chat="")]])
        await iquery.answer(msg, show_alert=True)
        if stark[2] == "one":
            if id == int(stark[1]):
                await iquery.edit_message_text("💌 ᴡʜɪsᴘᴇʀ ʜᴀs ʙᴇᴇɴ ʀᴇᴀᴅ !\n\nᴘʀᴇss ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴇɴᴅ ᴡʜɪsᴘᴇʀ !", reply_markup=SWITCH)
    except Exception as e:
        await iquery.answer(str(e), show_alert=True)
