import random
from datetime import datetime
from FallenRobot import pbot as pgram
from FallenRobot import DRAGONS as SUPREME_USERS
from pyrogram import filters
from FallenRobot.modules.mongo.couples_db import get_couple,save_couple,del_couple

def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a

tomorrow = str(dt_tom())
today = str(dt()[0])


CAP = """
**💌 ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ : :**\n
{0} + {1} = 💘\n
`ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {2}`
"""
COUPLES_PIC = "https://graph.org/file/92f6c0af097288607ab73.jpg"


@pgram.on_message(filters.command("scouple") & filters.group)
async def _chutiya(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return
    chat_id = message.chat.id
    if len(message.command) != 3:
        return await message.reply_text("**ʜᴇʏ ᴍᴀsᴛᴇʀ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ɢɪᴠᴇ ᴍᴇ ᴛᴡᴏ ᴜsᴇʀs ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ**")
    is_selected = await get_couple(chat_id, today)
    user1 = int(message.command[1]) if message.command[1].isdigit() else str(message.command[1]) 
    user2 = int(message.command[2]) if message.command[2].isdigit() else str(message.command[2]) 
    try :
        papa = (await _.get_chat_member(chat_id,user1)).user.id
        mumma = (await _.get_chat_member(chat_id,user2)).user.id
    except Exception as e:
        return await message.reply_text(e)  
    if not is_selected:
        couple = {"c1_id": papa, "c2_id": mumma}
        await save_couple(chat_id, today, couple)        
    elif is_selected:
        await del_couple(chat_id)
        couple = {"c1_id": papa, "c2_id": mumma}
        await save_couple(chat_id, today, couple)
    return await message.reply_text("**sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ ᴅᴏ /couple ᴛᴏ ɢᴇᴛ ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ**")        

                         

@pgram.on_message(filters.command(["couple","couples","shipping"]) & ~filters.private)
async def nibba_nibbi(_, message):    
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in _.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                return await message.reply_text("ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await _.get_users(c1_id)).mention
            c2_mention = (await _.get_users(c2_id)).mention
            await _.send_photo(message.chat.id,photo=COUPLES_PIC, caption=CAP.format(c1_mention,c2_mention,tomorrow))    
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])  
            try:              
                c1_mention = (await _.get_users(c1_id)).mention 
                c2_mention = (await _.get_users(c2_id)).mention
                
                couple_selection_message = f"""**💌 ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ :**
{c1_mention} + {c2_mention} = 💘
`ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏf ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {tomorrow}`"""
                await _.send_photo(message.chat.id,photo=COUPLES_PIC,caption=couple_selection_message)
            except :
                couple_selection_message = f"""**💌 ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ :**
{c1_id} + {c1_id} = 💘
`ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏf ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {tomorrow}`"""
                await _.send_photo(message.chat.id,photo=COUPLES_PIC,caption=couple_selection_message)
    except Exception as e:
        print(e)
        await message.reply_text(e)
