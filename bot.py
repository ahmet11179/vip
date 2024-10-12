import re
from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv
from pyrogram import Client, filters

load_dotenv()

# API ve MongoDB bilgileri
API_ID = int(getenv("API_ID", "26400244"))
API_HASH = getenv("API_HASH", "5e69daaa3668a56fe9b72319b280c071")
BOT_TOKEN = getenv("BOT_TOKEN", "6659155018:AAHLnw8kM2s_HIM47WULqRk6QfASe0V-NJo")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://botmuzik654:muziks@cluster0.5ory5au.mongodb.net/?retryWrites=true&w=majority")

# MongoDB bağlantısı
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client["bot_database"]  # Veritabanı adı
groups_collection = db["groups"]  # Grupları kaydedeceğimiz koleksiyon

# Grup kaydetme fonksiyonu
def save_group(chat_id, title):
    if not groups_collection.find_one({"chat_id": chat_id}):
        groups_collection.insert_one({"chat_id": chat_id, "title": title})
        print(f"Grup kaydedildi: {title} ({chat_id})")
    else:
        print(f"Grup zaten kayıtlı: {title} ({chat_id})")

# Bot istemcisi
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message):
    # Mevcut grupları kaydet
    async for dialog in client.get_dialogs():
        if dialog.chat.type in ['group', 'supergroup']:
            save_group(dialog.chat.id, dialog.chat.title)
    await message.reply("Mevcut gruplar başarıyla kaydedildi!")

@app.on_message(filters.new_chat_members)
async def new_group(client: Client, message):
    chat_id = message.chat.id
    title = message.chat.title
    save_group(chat_id, title)
    await message.reply(f"Grup başarıyla kaydedildi: {title}")

# Botu başlatma
app.run()