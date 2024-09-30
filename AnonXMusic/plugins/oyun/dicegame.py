from pyrogram import Client, enums, filters
import asyncio
from AnonXMusic import app as app

@app.on_message(filters.command("zar"))
async def dice(bot, message):
    x = await bot.send_dice(message.chat.id)  # Zar atılır
    m = x.dice.value  # Zarın sonucu alınır
    await message.reply_text(f"Hey {message.from_user.mention}, puanınız: {m}", quote=True)  # Sonuç kullanıcıya gönderilir
  
@app.on_message(filters.command("dart"))
async def dart(bot, message):
    x = await bot.send_dice(message.chat.id, "🎯")  # Dart oyunu
    m = x.dice.value  # Sonuç alınır
    await message.reply_text(f"Hey {message.from_user.mention}, puanınız: {m}", quote=True)

@app.on_message(filters.command("basket"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "🏀")  # Basketbol oyunu
    m = x.dice.value  # Sonuç alınır
    await message.reply_text(f"Hey {message.from_user.mention}, puanınız: {m}", quote=True)

@app.on_message(filters.command("sulot"))
async def jackpot(bot, message):
    x = await bot.send_dice(message.chat.id, "🎰")  # Jackpot (slot makinesi)
    m = x.dice.value  # Sonuç alınır
    await message.reply_text(f"Hey {message.from_user.mention}, puanınız: {m}", quote=True)

@app.on_message(filters.command("Bowling"))
async def ball(bot, message):
    x = await bot.send_dice(message.chat.id, "🎳")  # Bowling oyunu
    m = x.dice.value  # Sonuç alınır
    await message.reply_text(f"Hey {message.from_user.mention}, puanınız: {m}", quote=True)

@app.on_message(filters.command("football"))
async def football(bot, message):
    x = await bot.send_dice(message.chat.id, "⚽")  # Futbol oyunu
    m = x.dice.value  # Sonuç alınır
    await message.reply_text(f"Hey {message.from_user.mention}, puanınız: {m}", quote=True)

__help__ = """
Emoji ile Oyun Oynayın:
/zar - Zar 🎲
/dart - Dart 🎯
/basket - Basketbol 🏀
/Bowling - Bowling 🎳
/football - Futbol ⚽
/sulot - Slot makinesi döndür 🎰
"""

__mod_name__ = "Dɪᴄᴇ"
