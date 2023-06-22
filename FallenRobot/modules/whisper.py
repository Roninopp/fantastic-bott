from FallenRobot import pbot as pgram,BOT_USERNAME
from pyrogram import filters

from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)


whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ’Œ sá´‡É´á´… á´€ á´¡ÊœÉªsá´˜á´‡Ê€",switch_inline_query_current_chat=".whisper")]])


async def _whisper(_,inline_query):       
    data = inline_query.query
    results = []    
    if len(data.split()) < 3:
        mm = [InlineQueryResultArticle(title="á´¡ÊœÉªsá´˜á´‡Ê€", description=f"@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]", input_message_content=InputTextMessageContent(f"ðŸ’Œ á´œsá´€É¢á´‡ :\n\n@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]"), thumb_url="https://graph.org/file/2c3c693d1b460c309da1d.jpg",reply_markup=switch_btn)]
    else:        
        try:
            user_id = data.split()[1]
            msg = data.split(None,2)[2]
        except IndexError as e:
            pass
        try:
            user = await _.get_users(user_id)
        except:
            mm = [InlineQueryResultArticle(title="á´¡ÊœÉªsá´˜á´‡Ê€", description="iÉ´á´ á´€ÊŸÉªá´… á´œsá´‡Ê€É´á´€á´á´‡ á´Ê€ iá´… !", input_message_content=InputTextMessageContent("IÉ´á´ á´€ÊŸÉªá´… á´œsá´‡Ê€É´á´€á´á´‡ á´Ê€ Iá´… !"),thumb_url="https://graph.org/file/14782c2116addc0537bce.jpg",reply_markup=switch_btn)]
        
        try:        
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ’Œ á´¡ÊœÉªsá´˜á´‡Ê€",callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            mm = [InlineQueryResultArticle(title="á´¡ÊœÉªsá´˜á´‡Ê€", description=f"sá´‡É´á´… á´€ á´¡ÊœÉªsá´˜á´‡Ê€ á´›á´ {user.first_name} !", input_message_content=InputTextMessageContent(f"ðŸ’Œ á´€ á´¡ÊœÉªsá´˜á´‡Ê€ Êœá´€s Ê™á´‡á´‡É´ sá´‡É´á´› á´›á´ {user.first_name}.\n\ná´É´ÊŸÊ Êœá´‡/sÊœá´‡ á´„á´€É´ á´á´˜á´‡É´ Éªá´›."), thumb_url="https://graph.org/file/2c3c693d1b460c309da1d.jpg",reply_markup=whisper_btn)]       
        except Exception as e:
            print(e)
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
    if user_id not in [from_user,to_user]:
        return await query.answer("á´›ÊœÉªs á´¡ÊœÉªsá´˜á´‡Ê€ Éªs É´á´á´› Ò“á´Ê€ Êá´á´œ ðŸš§", show_alert=True)
    search_msg = f"{from_user}_{to_user}"
    try:
        msg = whisper_db[search_msg] 
    except:
        msg = "ðŸš« á´‡Ê€Ê€á´Ê€ â€¼ï¸\n\ná´¡ÊœÉªsá´˜á´‡Ê€ Êœá´€s Ê™á´‡á´‡É´ á´…á´‡ÊŸá´‡á´›á´‡á´… Ò“Ê€á´á´ Dá´€á´›á´€Ê™á´€sá´‡ !"
    await query.answer(msg, show_alert=True)
