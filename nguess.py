import time
import random
import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from NGUESS.db import user_collection, collection
from NGUESS import NGUESS
from config import GROUP_IDS, GUESS_TIMEOUT

# Global Session Tracker
ongoing_sessions = {}
streak_data = {}

def sc(text: str):
    small = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tiny  = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(tiny[small.index(c)] if c in small else c for c in text)

async def check_timeout(chat_id: int, message: Message, round_id: float):
    """Ghost Timer Prevention: Only triggers if the round_id matches."""
    await asyncio.sleep(GUESS_TIMEOUT)
    session = ongoing_sessions.get(chat_id)
    
    if session and session.get("round_id") == round_id and not session.get("guessed"):
        char = session.get("character")
        name = char.get('name', 'Unknown')
        await message.reply(sc(f"⏰ ᴛɪᴍᴇ ᴏᴠᴇʀ! ᴛʜᴇ ᴀɴsᴡᴇʀ ᴡᴀs: {name}"))
        ongoing_sessions.pop(chat_id, None)

async def spawn_game(message: Message, chat_id: int):
    """Fetch and send the next character."""
    total = await collection.count_documents({})
    if total == 0: return
    
    char = await collection.find_one(skip=random.randint(0, total-1))
    round_id = time.time() # Unique ID for this round
    
    ongoing_sessions[chat_id] = {
        "character": char, 
        "round_id": round_id, 
        "guessed": False
    }

    caption = f"✨ {sc('Guess the character!')}\n⏳ {GUESS_TIMEOUT} s"
    await message.reply_photo(char["img_url"], caption=caption)
    asyncio.create_task(check_timeout(chat_id, message, round_id))

@NGUESS.on_message(filters.command("nguess") & filters.group)
async def start_cmd(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in GROUP_IDS: return
    if chat_id in ongoing_sessions:
        return await message.reply(sc("❌ ᴀ ɢᴀᴍᴇ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ!"))
    await spawn_game(message, chat_id)

@NGUESS.on_message(filters.text & filters.group & ~filters.command(["nguess", "bal"]))
async def handle_guess(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in ongoing_sessions: return
    
    session = ongoing_sessions[chat_id]
    if session.get("guessed"): return

    guess = message.text.strip().lower()
    correct_name = session["character"]["name"].strip().lower()

    # FIX: Recognition Logic
    if re.search(r'\b' + re.escape(correct_name) + r'\b', guess):
        session["guessed"] = True # Stops the timer
        user_id = message.from_user.id
        
        coins = random.randint(20, 50)
        await user_collection.update_one({"id": user_id}, {"$inc": {"coins": coins}}, upsert=True)

        if chat_id not in streak_data: streak_data[chat_id] = 0
        streak_data[chat_id] += 1
        
        await message.reply(sc(f"🎉 ᴄᴏʀʀᴇᴄᴛ! +{coins} ᴄᴏɪɴs!\n🎭 ɴᴀᴍᴇ: {correct_name.upper()}\n🔥 sᴛʀᴇᴀᴋ: {streak_data[chat_id]}"))
        
        await asyncio.sleep(2) # Prevent spamming
        await spawn_game(message, chat_id)
