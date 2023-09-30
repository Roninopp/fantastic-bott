from telethon import events
from . import telethn

@telethn.on(events.NewMessage(pattern=r"^/(alive|about|hosting)"))
async def about(event):
    await event.reply("Bot is working fine!\nHosted by @SpiralTechDivision")
