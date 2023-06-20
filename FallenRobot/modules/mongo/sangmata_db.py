from FallenRobot.utils.mongo import db

matadb = db.sangmata


# Get Data User
async def cek_userdata(user_id: int) -> bool:
    user = await matadb.find_one({"user_id": user_id})
    return bool(user)


async def get_enabled_chat_ids():
    chats_cursor = matadb.find({"chat_id_toggle": {"$exists": True}})
    chats = await chats_cursor.to_list(length=None)
    return [chat["chat_id_toggle"] for chat in chats]

async def get_userdata(user_id: int, chat_id: int):
    user = await matadb.find_one({"user_id": user_id, "chat_id": chat_id})
    if user:
        return user.get("username"), user.get("first_name"), user.get("last_name")
    return None, None, None


async def add_userdata(user_id: int, chat_id: int, username, first_name, last_name):
    await matadb.update_one({"user_id": user_id, "chat_id": chat_id}, {"$set": {"username": username, "first_name": first_name, "last_name": last_name}}, upsert=True)


# Enable Mata MissKaty in Selected Chat
async def is_sangmata_on(chat_id: int) -> bool:
    chat = await matadb.find_one({"chat_id_toggle": chat_id})
    return bool(chat)


async def sangmata_on(chat_id: int) -> bool:
    await matadb.insert_one({"chat_id_toggle": chat_id})


async def sangmata_off(chat_id: int):
    await matadb.delete_one({"chat_id_toggle": chat_id})
