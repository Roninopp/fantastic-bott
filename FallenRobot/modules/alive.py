import asyncio
import datetime
from datetime import datetime

from telegram import __version__ as ptb
from telethon import Button

from FallenRobot import BOT_NAME, BOT_USERNAME, SUPPORT_CHAT
from FallenRobot import telethn as neko
from FallenRobot.events import register

edit_time = 5
""" =======================Neko====================== """
file1 = "https://telegra.ph/file/da817befa131f7a5f533e.jpg"
file2 = "https://telegra.ph/file/a048c4fa0bdb2738fff69.jpg"
file3 = "https://telegra.ph/file/a62029574186f318c6529.jpg"
file4 = "https://telegra.ph/file/1368985b1a20870949673.jpg"
file5 = "https://telegra.ph/file/7dcde6edba760c620e91f.jpg"
""" =======================Neko====================== """

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)


@register(pattern=("/alive"))
async def hmm(yes):
    await yes.get_chat()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    NekoX = f"**👋Hey there [{yes.sender.first_name}](tg://user?id={yes.sender.id})\n\n🌟I'm {BOT_NAME}\n💐I'm Functioning Flawlessly Darling💕 **\n\n"
    NekoX += f"**🔸My Uptime:🔸** `{uptime}`\n\n"
    NekoX += f"**🔸PTB Version :🔸** `{ptb}`\n\n"
    BUTTON = [
        [
            Button.url("🚑Support", f"https://t.me/{SUPPORT_CHAT}"),
        ]
    ]
    await neko.send_file(yes.chat_id, file="https://graph.org/file/304a79291fcb8d9ca9cdf.mp4",caption=NekoX, buttons=BUTTON)
