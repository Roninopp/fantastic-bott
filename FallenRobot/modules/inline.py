import time 
import html
import json
import requests 
import random 
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
)
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from FallenRobot import pbot as pgram,BOT_ID
from FallenRobot.modules.whisper import _whisper

keywards = InlineKeyboardMarkup([[
InlineKeyboardButton("sᴇɴᴅ ᴡʜɪsᴘᴇʀ",switch_inline_query_current_chat=".whisper")]])

async def in_help():
    answers = [
         InlineQueryResultArticle("Help Menu!",
         InputTextMessageContent("Inline Commands!"),
         thumb_url="https://graph.org/file/f6278ec869dbb1eebfe0e.jpg",
         reply_markup=keywards)]
    return answers

@pgram.on_inline_query()
async def botinline(_, inline_query):
    string = inline_query.query.lower()
    if string.strip() == "":
        answers = await in_help()
        await inline_query.answer(answers)
    elif string.split()[0] == ".whisper":
        answers = await _whisper(_,inline_query)
        await inline_query.answer(answers[-1], cache_time=0)
