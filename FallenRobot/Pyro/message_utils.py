import asyncio
from logging import getLogger

from pyrogram.errors import ChatWriteForbidden, FloodWait, MessageNotModified, ChatAdminRequired, MessageDeleteForbidden, MessageIdInvalid, MessageEmpty
from FallenRobot import pbot as app

LOGGER = getLogger(__name__)

# handler for TG function, so need write exception in every code


# Send MSG Pyro
async def kirimPesan(chat, text, **kwargs):
    try:
        return await app.send_message(chat_id=chat.id, text=text, **kwargs)
    except FloodWait as e:
        LOGGER.warning(str(e))
        await asyncio.sleep(e.x)
        return await kirimPesan(chat, text, **kwargs)
    except (ChatWriteForbidden, ChatAdminRequired):
        LOGGER.info(f"Leaving from {chat.title} [{chat.id}] because it doesn't have admin permission.")
        return await app.leave_chat(chat.id)
    except Exception as e:
        LOGGER.error(str(e))
        return


# Edit MSG Pyro
async def editPesan(msg, text, **kwargs):
    try:
        return await msg.edit(text, **kwargs)
    except FloodWait as e:
        LOGGER.warning(str(e))
        await asyncio.sleep(e.value)
        return await editPesan(msg, text, **kwargs)
    except (MessageNotModified, MessageIdInvalid, MessageEmpty):
        return
    except Exception as e:
        LOGGER.error(str(e))
        return


async def hapusPesan(msg):
    try:
        return await msg.delete()
    except (MessageDeleteForbidden, ChatAdminRequired):
        return
    except FloodWait as e:
        LOGGER.warning(str(e))
        await asyncio.sleep(e.value)
        return await hapusPesan(msg)
    except Exception as e:
        LOGGER.error(str(e))
