import os
import re
import sys
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch

# Telegram API ayarları
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Pyrogram client oluştur
app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# "/bul" komutunu işle
@app.on_message(filters.command("bul"))
async def search_music(client, message: Message):
    # Mesajın içeriğini al
    query = " ".join(message.command[1:])
    
    # Query boşsa kullanıcıya bilgi ver ve çık
    if not query:
        await message.reply("Lütfen aramak istediğiniz sanatçının ismini girin.")
        return
    
    # Youtube'da arama yap
    results = YoutubeSearch(query, max_results=5).to_dict()
    
    # Sonuçları kullanıcıya gönder
    if results:
        reply_text = "İşte aradığınız sanatçının videoları:\n"
        for video in results:
            reply_text += f"{video['title']} - [İndir]({video['url_suffix']})\n"
    else:
        reply_text = "Üzgünüm, arama sonuçları bulunamadı."
    
    # Kullanıcıya cevap ver
    await message.reply_text(reply_text, disable_web_page_preview=True)

# Client'i başlat
app.run()