from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from FallenRobot import pbot as app
import json
import time
import random

with open('trivia.json') as f:
    data = json.load(f)

active_trivia = {} 

@app.on_message(filters.group & filters.command('trivia'), group=84)
async def trivia(_, message):
    user_id = message.from_user.id

    if user_id in active_trivia:
        await message.reply_text("You already have an active trivia session.")
        return

    quesdata = random.choice(data['results'])
    question = quesdata["question"]
    correct_answer = quesdata["correct_answer"]
    incorrect_answers = quesdata['incorrect_answers']
    all_options = incorrect_answers + [correct_answer]
    random.shuffle(all_options)

    button_list = [
        [InlineKeyboardButton(option.capitalize(), callback_data=f"answer_{option.strip().lower()}")]
        for option in all_options
    ]

    await message.reply_text(
        question,
        reply_markup=InlineKeyboardMarkup(button_list)
    )

    active_trivia[user_id] = {
        "correct_answer": correct_answer.lower(),
        "expiration_time": time.time() + 60 
    }

@app.on_callback_query()
async def handle_callback_query(client, query: CallbackQuery):
    selected_option = query.data.split('_')[1]
    user_id = query.from_user.id

    active_session = active_trivia.get(user_id)
    
    if not active_session:
        return

    correct_option = active_session["correct_answer"]

    if time.time() > active_session["expiration_time"]:
        await query.message.edit_text("Trivia session has expired.")
        active_trivia.pop(user_id, None)
        return

    response_text = "Correct! 🎉" if selected_option == correct_option else "Incorrect. Try again! ❌"
    await query.message.edit_text(query.message.text + f"\n\n{response_text}")

    active_trivia.pop(user_id, None)
