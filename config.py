import os
from pyrogram import filters

API_ID = int(os.getenv("API_ID", "21218274"))
API_HASH = os.getenv("API_HASH", "3474a18b61897c672d315fb330edb213")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8369315494:AAGDRxnSla830eH-M-4Oqh4-KnEk5tibLeA")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot")

# Fix: Handles spaces in the comma-separated string
raw_groups = os.getenv("GROUP_IDS", "-1002619782493, -1002691911300")
GROUP_IDS = [int(gid.strip()) for gid in raw_groups.split(",")]

GUESS_TIMEOUT = 30  # Speed up to 30s for better gameplay
