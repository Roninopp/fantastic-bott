from pyrogram import *
from pyrogram.types import *
from FallenRobot import pbot as app

@app.on_message(filters.command(["start","help"]) & filters.private)
async def shity_af_stuff(client : Client,message : Message) :
    try : 
        await client.send_message(-1001966188512,f"{message.from_user.mention} #FANTASTIC_BOT New User Just Started The Bot In Pm")
    except Exception :
        pass
