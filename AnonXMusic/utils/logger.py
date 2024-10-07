from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ParseMode
from AnonXMusic import app
from config import LOGGER_ID


@app.on_chat_member_updated()
async def handle_chat_member_update(client, update):
    # Botun gruptan atılması durumu
    if update.new_chat_member.status == ChatMemberStatus.KICKED:
        log_text = f"""
<b>AnonXMusic Bot Gruptan Atıldı!</b>

<b>Grup ID:</b> <code>{update.chat.id}</code>
<b>Grup Adı:</b> {update.chat.title}
<b>Grup Linki:</b> @{update.chat.username}

<b>Atan Kişi:</b> {update.from_user.mention}
<b>Kişi ID:</b> <code>{update.from_user.id}</code>
"""
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=log_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"Log mesajı gönderilemedi: {e}")

        # Burada botu gruptan çıkaracak bir işlem yok, 
        # çünkü Telegram API, botun kendisini koruma işlevi sağlamaz.
        return
    # Botun gruba eklenmesi durumu
    elif update.new_chat_member.status == ChatMemberStatus.MEMBER:
        log_text = f"""
<b>AnonXMusic Bot Gruba Eklendi!</b>

<b>Grup ID:</b> <code>{update.chat.id}</code>
<b>Grup Adı:</b> {update.chat.title}
<b>Grup Linki:</b> @{update.chat.username}

<b>Ekleme Yapan Kişi:</b> {update.from_user.mention}
<b>Kişi ID:</b> <code>{update.from_user.id}</code>
"""
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=log_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"Log mesajı gönderilemedi: {e}")