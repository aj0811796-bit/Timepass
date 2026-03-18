from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo_url = os.getenv("MONGO_URL")
ddw = AsyncIOMotorClient(mongo_url)
db = ddw['hinata_waifu']

# Aliases
collection = db['gaming_anime_characters']  # Your characters
user_collection = db['gamimg_user_collection'] # Your users
