# Written by github.com/krrish557
from FallenRobot import pbot as app
from pyrogram import filters
from pyrogram.types import Message
from FallenRobot.planetScale_sqlDB.playerDB import check_user
from FallenRobot.planetScale_sqlDB.helper_function.create import create
from FallenRobot.planetScale_sqlDB.helper_function.read import read
from FallenRobot.planetScale_sqlDB.helper_function.update import update
from FallenRobot.utils.custom_filters import command
import datetime
import re
import random
import asyncio

reader = read()
updater = update()
creater = create()
userdict = {}
DART_DICT = {}
BOWL_DICT = {}
BASKET_DICT = {}
DICE_DICT = {}
GOAL_DICT = {}
BET_DICT = {}


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


async def get_user_won(emoji, value):
    if emoji in ['🎯', '🎳']:
        if value >= 4:
            u_won = True
        else:
            u_won = False
    elif emoji in ['🏀', '⚽']:
        if value >= 3:
            u_won = True
        else:
            u_won = False
    return u_won


async def can_play(tame, tru):
    current_time = datetime.datetime.now()
    time_since_last_collection = current_time - \
        datetime.datetime.fromtimestamp(tame)
    x = tru - time_since_last_collection.total_seconds()
    if str(x).startswith('-'):
        return 0
    return x


@app.on_message(filters.command("dart")) 
async def dart(client, message):
    try:
        bet = int(message.text.split()[1])
    except IndexError:
        await message.reply_text("Enter a valid amount!")
        return
    if bet > 1000000 or bet <= 0:
        await message.reply_text("You can not bet more then 10 Lakhs or less then 1 ruby")
        return
    if bet > reader.ruby(message.from_user.id):
        await message.reply_text("You can not bet more money then you have in your wallet")
        return
    if check_user(message.from_user.id):
        chat_id = message.chat.id
        user = message.from_user
        if user.id not in DART_DICT.keys():
            DART_DICT[user.id] = None
        if DART_DICT[user.id]:
            x = await can_play(DART_DICT[user.id], 20)
            if int(x) != 0:
                return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴅᴀʀᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')

        m = await client.send_dice(chat_id, '🎯')
        msg = await message.reply('....')
        u_won = await get_user_won(m.dice.emoji, m.dice.value)
        DART_DICT[user.id] = datetime.datetime.now().timestamp()
        if not u_won:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) - bet
            updater.add_money(user, new_wallet)
            await msg.edit_text(f"🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ• {bet} rubies")
        else:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) + bet
            updater.add_money(user, new_wallet)
            await msg.edit_text(f"✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ• {bet} Rubies Added to your Wallet.")
    else:
        creater.add_player_db(message.from_user.id, message.from_user.username)
        await message.reply_text("Try Again! \nYou were not found in our records but now I have recorded your info!")


@app.on_message(filters.command("slot")) 
async def slot(client: app, message: Message):
    try:
        bet = int(message.text.split()[1])
    except IndexError:
        await message.reply_text("Enter a valid amount!")
        return
    if bet > 1000000 or bet <= 0:
        await message.reply_text("You can not bet more then 10 Lakhs or less then 1 ruby")
        return
    if bet > reader.ruby(message.from_user.id):
        await message.reply_text("You can not bet more money then you have in your wallet")
        return
    if check_user(message.from_user.id):
        emoji = "🎰"
        numbers = [random.randint(0, 9) for _ in range(3)]
        result = " ".join(str(num) for num in numbers)
        if len(set(numbers)) == 1:
            new_wallet = reader.ruby(message.from_user.id) + bet
            updater.add_money(message.from_user.id, new_wallet)
            await message.reply_text(text=f"{emoji} {result}\nCongratulations! You Won {bet} rubies!")
        else:
            new_wallet = reader.ruby(message.from_user.id) - bet
            updater.add_money(message.from_user.id, new_wallet)
            await message.reply_text(text=f"{emoji} {result}\nBetter luck next time! You lost {bet} rubies")
    else:
        creater.add_player_db(message.from_user.id, message.from_user.username)
        await message.reply_text("Try Again! \nYou were not found in our records but now I have recorded your info!")


@app.on_message(filters.command("bowl")) 
async def bowl(client, message: Message):
    try:
        bet = int(message.text.split()[1])
    except IndexError:
        await message.reply_text("Enter a valid amount!")
        return
    if bet > 1000000 or bet <= 0:
        await message.reply_text("You can not bet more then 10 Lakhs or less then 1 ruby")
        return
    if bet > reader.ruby(message.from_user.id):
        await message.reply_text("You can not bet more money then you have in your wallet")
        return
    if check_user(message.from_user.id):
        chat_id = message.chat.id
        user = message.from_user
        if user.id not in BOWL_DICT.keys():
            BOWL_DICT[user.id] = None
        if BOWL_DICT[user.id]:
            x = await can_play(BOWL_DICT[user.id], 20)
            if int(x) != 0:
                return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ Bowl ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')

        m = await client.send_dice(chat_id, '🎳')
        msg = await message.reply('....')
        u_won = await get_user_won(m.dice.emoji, m.dice.value)
        BOWL_DICT[user.id] = datetime.datetime.now().timestamp()
        if not u_won:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) - bet
            try:
                updater.add_money(user, new_wallet)
            except Exception as e:
                print(e)

            return await msg.edit("🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ• ")
        else:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) + bet
            try:
                updater.add_money(user, new_wallet)
            except Exception as e:
                print(e)
            return await msg.edit(f"✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ• {bet} rubies have been added to your Wallet.")
    else:
        creater.add_player_db(message.from_user.id, message.from_user.username)
        await message.reply_text("Try Again! \nYou were not found in our records but now I have recorded your info!")
        return


@app.on_message(filters.command("basket")) 
async def basket(client, message):
    try:
        bet = int(message.text.split()[1])
    except IndexError:
        await message.reply_text("Enter a valid amount!")
        return
    if bet > 1000000 or bet <= 0:
        await message.reply_text("You can not bet more then 10 Lakhs or less then 1 ruby")
        return
    if bet > reader.ruby(message.from_user.id):
        await message.reply_text("You can not bet more money then you have in your wallet")
        return

    if check_user(message.from_user.id):
        chat_id = message.chat.id
        user = message.from_user
        if user.id not in BASKET_DICT.keys():
            BASKET_DICT[user.id] = None
        if BASKET_DICT[user.id]:
            x = await can_play(BASKET_DICT[user.id], 20)
            if int(x) != 0:
                return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ Basket ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')

        m = await client.send_dice(chat_id, '🏀')
        msg = await message.reply('....')
        u_won = await get_user_won(m.dice.emoji, m.dice.value)
        BASKET_DICT[user.id] = datetime.datetime.now().timestamp()
        if not u_won:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) - bet
            updater.add_money(user, new_wallet)
            return await msg.edit("🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ• ")
        else:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) + bet
            updater.add_money(user, new_wallet)
            return await msg.edit(f"✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ• {bet} rubies have been added to your Wallet.")
    else:
        creater.add_player_db(message.from_user.id, message.from_user.username)
        await message.reply_text("Try Again! \nYou were not found in our records but now I have recorded your info!")


@app.on_message(filters.command("goal")) 
async def GOAL(client, message):
    try:
        bet = int(message.text.split()[1])
    except IndexError:
        await message.reply_text("Enter a valid amount!")
        return
    if bet > 1000000 or bet <= 0:
        await message.reply_text("You can not bet more then 10 Lakhs or less then 1 ruby")
        return
    if bet > reader.ruby(message.from_user.id):
        await message.reply_text("You can not bet more money then you have in your wallet")
        return
    if check_user(message.from_user.id):
        chat_id = message.chat.id
        user = message.from_user
        if user.id not in GOAL_DICT.keys():
            GOAL_DICT[user.id] = None
        if GOAL_DICT[user.id]:
            x = await can_play(GOAL_DICT[user.id], 20)
            if int(x) != 0:
                return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ GOAL ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')

        m = await client.send_dice(chat_id, '⚽')
        msg = await message.reply('....')
        u_won = await get_user_won(m.dice.emoji, m.dice.value)
        GOAL_DICT[user.id] = datetime.datetime.now().timestamp()
        if not u_won:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) - bet
            updater.add_money(user, new_wallet)
            return await msg.edit("🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ• ")
        else:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) + bet
            updater.add_money(user, new_wallet)
            return await msg.edit(f"✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ• {bet} rubies have been added to your Wallet.")
    else:
        creater.add_player_db(message.from_user.id, message.from_user.username)
        await message.reply_text("Try Again! \nYou were not found in our records but now I have recorded your info!")


@app.on_message(filters.command("dice")) 
async def DICE(client, message):
    try:
        bet = int(message.text.split()[1])
        amount = int(message.text.split()[2])
    except IndexError:
        await message.reply_text("Enter a valid amount!")
        return
    if amount > 1000000 or amount <= 0:
        await message.reply_text("You can not bet more then 10 Lakhs or less then 1 ruby")
        return
    if bet < 1 or bet > 6:
        await message.reply_text("Bet between 1 to 6 only")
        return

    if check_user(message.from_user.id):
        chat_id = message.chat.id
        user = message.from_user
        if user.id not in DICE_DICT.keys():
            DICE_DICT[user.id] = None
        if DICE_DICT[user.id]:
            x = await can_play(DICE_DICT[user.id], 20)
            if int(x) != 0:
                return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ DICE ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')

        m = await client.send_dice(chat_id, '🎲')
        msg = await message.reply('....')
        if m.dice.value == bet:
            u_won = True
        else:
            u_won = False
        DICE_DICT[user.id] = datetime.datetime.now().timestamp()
        if not u_won:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) - amount
            updater.add_money(user, new_wallet)
            return await msg.edit("🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ• ")
        else:
            await asyncio.sleep(5)
            new_wallet = reader.ruby(user.id) + amount
            updater.add_money(user, new_wallet)
            return await msg.edit(f"✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ• {amount} rubies have been added to your Wallet.")
    else:
        creater.add_player_db(message.from_user.id, message.from_user.username)
        await message.reply_text("Try Again! \nYou were not found in our records but now I have recorded your info!")


@app.on_message(filters.command("bet")) 
async def _bet(client, message):
    chat_id = message.chat.id
    user = message.from_user
    if not check_user(user.id):
        creater.add_player_db(user.id, user.username)
    if user.id not in BET_DICT.keys():
        BET_DICT[user.id] = None
    if BET_DICT[user.id]:
        x = await can_play(BET_DICT[user.id], 12)
        print(x)
        if int(x) != 0:
            return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ʙᴇᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ {get_readable_time(x)}.')
    possible = ['h', 'heads', 'tails', 't', 'head', 'tail']
    if len(message.command) < 3:
        return await message.reply_text("✑ ᴜsᴀɢᴇ : /bet [ʜᴇᴀᴅs/ᴛᴀɪʟs] [ᴀᴍᴏᴜɴᴛ]")
    cmd = message.command[1].lower()
    to_bet = message.command[2]
    coins = reader.ruby(user.id)
    if to_bet == '*':
        to_bet = coins
    elif not to_bet.isdigit():
        return await message.reply_text("ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
    to_bet = int(to_bet)
    if to_bet == 0:
        return await message.reply_text("ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ? ʟᴏʟ!")
    elif to_bet > coins:
        return await message.reply_text(f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ rubies ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{coins}` rubies")
    rnd = random.choice(['heads', 'tails'])
    if cmd not in possible:
        return await message.reply_text("ʏᴏᴜ sʜᴏᴜʟᴅ ᴛʀʏ ʜᴇᴀᴅs ᴏʀ ᴇɪᴛʜᴇʀ ᴛᴀɪʟs.")
    if cmd in ['h', 'head', 'heads']:
        if rnd == 'heads':
            user_won = True
        else:
            user_won = False
    if cmd in ['t', 'tail', 'tails']:
        if rnd == 'tails':
            user_won = True
        else:
            user_won = False
    BET_DICT[user.id] = datetime.datetime.now().timestamp()
    if not user_won:
        new_wallet = coins - to_bet
        updater.add_money(user.id, new_wallet)
        return await message.reply_text("🛑 ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ {0}!\n• ʏᴏᴜ ʟᴏsᴛ `{1:,}` ᴄᴏɪɴs\n• ᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ : `{2:,}` rubies".format(rnd, to_bet, new_wallet))
    else:
        new_wallet = coins + to_bet
        updater.add_money(user.id, new_wallet)
        return await message.reply_text("✅ ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ {0}!\nʏᴏᴜ ᴡᴏɴ `{1:,}` ᴄᴏɪɴs\nᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ : `{2:,}` rubies".format(rnd, to_bet, new_wallet))

regex_upvote = r"(?i)^((\+|\+|\+1|thx|thanx|thanks|pro|cool|good|pro|pero|op|nice|noice|best|uwu|owo|right|correct|peru|piro|👍|\+100)$)"

regex_downvote = r"(?i)^((-|\-\-|\-1|👎|noob|baka|idiot|chutiya|nub|noob|wrong|incorrect|chaprii|chapri|weak|\-100)$)"


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=4,
)
async def upvote(client, message: Message):
    if not message.reply_to_message.from_user:
        return
    user = message.reply_to_message.from_user

    if not await check_user(user.id):
        await creater.add_player_db(user.id, user.username)
    if user.id == message.from_user.id:
        return
    coins = await reader.ruby(user.id)
    new = coins + 200
    updater.add_money(user.id, new)
    await message.reply_text("ᴀᴅᴅᴇᴅ `200` Rubies ᴛᴏ {0} ᴡᴀʟʟᴇᴛ.\n• ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` Rubies".format(user.mention, new))


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.me
    & ~filters.bot,
    group=3,
)
async def downvote(client, message: Message):
    if not message.reply_to_message.from_user:
        return
    user = message.reply_to_message.from_user

    if not await check_user(user.id):
        await creater.add_player_db(user.id)
    if user.id == message.from_user.id:
        return
    coins = await reader.ruby(user.id, user.username)
    if coins <= 0:
        return
    else:
        new = coins - 200
    updater.add_money(user.id, new)
    await message.reply_text("ᴛᴏᴏᴋ `200` Rubies ғʀᴏᴍ {𝟶} ᴡᴀʟʟᴇᴛ.\n• ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{𝟷:,}` Rubies".format(user.mention, new))
