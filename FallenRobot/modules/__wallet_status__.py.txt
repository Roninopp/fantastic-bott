from FallenRobot import pbot as app
from FallenRobot.planetScale_sqlDB.helper_function.read import read
from pyrogram import Client, filters
from pyrogram.types import Message
import json


reader = read()


@app.on_message(filters.command("wallet")) 
async def my_inventory(c: Client, m: Message):
    user_id = m.from_user.id
    rubies = reader.ruby(user_id)

    message = f"Rubies 💵: {rubies}\n"
    await m.reply_text(message)
