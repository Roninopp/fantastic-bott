from FallenRobot.utils.mongo import db

antichanneldb = db.antichannel

async def antichannelmode_on(chat_id : int):
    return await antichanneldb.insert_one({"chat_id" : chat_id}) 
  
async def antichannelmode_off(chat_id : int):
    return await antichanneldb.delete_one({"chat_id" : chat_id})
   
async def isModOn(chat_id : int) -> bool:
    return bool(await antichanneldb.find_one({"chat_id" : chat_id}))
  
