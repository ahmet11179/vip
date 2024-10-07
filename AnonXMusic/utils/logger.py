from pyrogram.enums import ParseMode
from AnonXMusic import app
from AnonXMusic.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>{app.mention} 𝗈𝗒𝗇𝖺𝗍𝗆𝖺 𝗅𝗈𝗀𝗎</b>

<b>𝖦𝗋𝗎𝗉 𝖨𝖽 :</b> <code>{message.chat.id}</code>
<b>𝖦𝗋𝗎𝗉 𝖠𝖽ı :</b> {message.chat.title}
<b>𝖦𝗋𝗎𝗉 𝖫𝗂𝗇𝗄𝗂 :</b> @{message.chat.username}

<b>𝖪𝗎𝗅𝗅𝖺𝗇ı𝖼ı 𝖨𝖽 :</b> <code>{message.from_user.id}</code>
<b>𝖪𝗎𝗅𝗹𝖺𝗇ı𝖼ı 𝖠𝖽ı :</b> {message.from_user.mention}
<b>𝖪𝗎𝗅𝗅𝖺𝗇ı𝖼ı 𝖫𝗂𝗇𝗄𝗂 :</b> @{message.from_user.username}

<b>𝖲𝗈𝗋𝗀𝗎 :</b> {message.text.split(None, 1)[1]}
<b>𝖠𝗄ı𝗌‌ 𝖳𝗎‌𝗋𝗎‌ :</b> {streamtype}"""

        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"Log mesajı gönderilemedi: {e}")
    return


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