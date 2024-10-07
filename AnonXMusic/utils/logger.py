from pyrogram.enums import ChatMemberStatus
from pyrogram import filters
from AnonXMusic import app
from config import LOGGER_ID


@app.on_my_chat_member()
async def handle_chat_member_update(client, message):
    # Botun gruba eklenmesi durumu
    if message.new_chat_member.status == ChatMemberStatus.MEMBER:
        log_text = f"""
<b>Bot Gruba Eklendi!</b>

<b>Grup ID:</b> <code>{message.chat.id}</code>
<b>Grup Adı:</b> {message.chat.title}
<b>Grup Linki:</b> @{message.chat.username}

<b>Ekleme Yapan Kişi:</b> {message.from_user.mention}
<b>Kişi ID:</b> <code>{message.from_user.id}</code>
"""
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=log_text,
                parse_mode="html",
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"Log mesajı gönderilemedi: {e}")

    # Botun gruptan atılması durumu
    elif message.new_chat_member.status == ChatMemberStatus.KICKED:
        log_text = f"""
<b>Bot Gruptan Atıldı!</b>

<b>Grup ID:</b> <code>{message.chat.id}</code>
<b>Grup Adı:</b> {message.chat.title}
<b>Grup Linki:</b> @{message.chat.username}

<b>Atan Kişi:</b> {message.from_user.mention}
<b>Kişi ID:</b> <code>{message.from_user.id}</code>
"""
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=log_text,
                parse_mode="html",
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"Log mesajı gönderilemedi: {e}")