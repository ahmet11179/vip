import os
import future
import asyncio
import requests
import wget
import time
import yt_dlp
from urllib.parse import urlparse
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from AnonXMusic import app, YouTube
from pyrogram import filters
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch
from youtubesearchpython import SearchVideos
import re
from pykeyboard import InlineKeyboard
from pyrogram.enums import ChatAction
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaAudio,
                            InputMediaVideo, Message)
from config import (BANNED_USERS, SONG_DOWNLOAD_DURATION,
                    SONG_DOWNLOAD_DURATION_LIMIT)
from AnonXMusic.utils.decorators.language import language, languageCB
from AnonXMusic.utils.formatters import convert_bytes
from AnonXMusic.utils.inline.song import song_markup

# Command
SONG_COMMAND = ["indir"]

@app.on_message(
    filters.command(SONG_COMMAND) & filters.group & ~BANNED_USERS
)
@language
async def song_command_group(client, message: Message, _):
    await message.delete()  # Mesajı grupta sil
    url = await YouTube.url(message)  # URL'yi al
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(_["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min))
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(_["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min))
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_message(
    filters.command(SONG_COMMAND) & filters.private & ~BANNED_USERS
)
@language
async def song_command_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(_["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min))
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(_["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min))
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_callback_query(
    filters.regex(pattern=r"song_back") & ~BANNED_USERS
)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(
    filters.regex(pattern=r"song_helper") & ~BANNED_USERS
)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass
    if stype == "audio":
        try:
            formats_available, link = await YouTube.formats(vidid, True)
        except:
            return await CallbackQuery.edit_message_text(_["song_7"])
        keyboard = InlineKeyboard()
        done = []
        for x in formats_available:
            check = x["format"]
            if "audio" in check and x["filesize"] is not None:
                form = x["format_note"].title()
                if form not in done:
                    done.append(form)
                    sz = convert_bytes(x["filesize"])
                    fom = x["format_id"]
                    keyboard.row(
                        InlineKeyboardButton(
                            text=f"{form} Quality Audio = {sz}",
                            callback_data=f"song_download {stype}|{fom}|{vidid}",
                        ),
                    )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"close"
            ),
        )
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=keyboard
        )
    else:
        try:
            formats_available, link = await YouTube.formats(vidid, True)
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text(_["song_7"])
        keyboard = InlineKeyboard()
        done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
        for x in formats_available:
            check = x["format"]
            if x["filesize"] is not None and int(x["format_id"]) in done:
                sz = convert_bytes(x["filesize"])
                ap = check.split("-")[1]
                to = f"{ap} = {sz}"
                keyboard.row(
                    InlineKeyboardButton(
                        text=to,
                        callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                    )
                )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"close"
            ),
        )
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=keyboard
        )

import yt_dlp
from pyrogram.types import InputMediaAudio, InputMediaVideo, ChatAction
from config import SUPPORT_CHAT

# Çerez dosyasını otomatik bulmak için fonksiyon
def cookiefile():
    cookie_dir = "cookies"
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        raise FileNotFoundError("Çerez dosyası bulunamadı. `cookies/` klasöründe .txt dosyası olmalı.")
    return os.path.join(cookie_dir, cookies_files[0])


@app.on_callback_query(
    filters.regex(pattern=r"song_download") & ~BANNED_USERS
)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("İndiriliyor...")
    except:
        pass

    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    thumb_image_path = await CallbackQuery.message.download()

    try:
        ydl_opts = {
            "quiet": True,
            "cookiefile": cookiefile(),  # çerez dosyasını otomatik kullan
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            x = ytdl.extract_info(yturl, download=False)
    except Exception as e:
        os.remove(thumb_image_path)
        return await CallbackQuery.edit_message_text(
            f"❌ YouTube içeriği alınamadı.\nGiriş gerekebilir veya bot doğrulama istiyor.\n\n🛠 Hata:\n`{e}`"
        )

    title = (x["title"]).title()
    duration = x.get("duration", 0)

    thank_you_message = (
        "🎵 Sonsuz Müzik kullandığınız için teşekkür ederiz!\n"
        "@sonsuzmuzik_bot ile müziğin ve filmlerin keyfini çıkarın."
    )

    if stype == "video":
        try:
            file_path = await YouTube.download(
                yturl, None, songvideo=True, format_id=format_id, title=title
            )
            med = InputMediaVideo(
                media=file_path,
                duration=duration,
                thumb=thumb_image_path,
                caption=thank_you_message,
                supports_streaming=True,
            )
        except Exception as e:
            os.remove(thumb_image_path)
            return await CallbackQuery.edit_message_text(_["song_9"].format(e))

        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=ChatAction.UPLOAD_VIDEO,
        )

        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            await CallbackQuery.edit_message_text(_["song_10"])
        finally:
            os.remove(file_path)

    elif stype == "audio":
        try:
            filename = await YouTube.download(
                yturl, None, songaudio=True, format_id=format_id, title=title
            )
            med = InputMediaAudio(
                media=filename,
                caption=thank_you_message,
                thumb=thumb_image_path,
                title=title,
                performer="@sonsuzmuzik_bot",
            )
        except Exception as e:
            os.remove(thumb_image_path)
            return await CallbackQuery.edit_message_text(_["song_9"].format(e))

        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=ChatAction.UPLOAD_AUDIO,
        )

        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            await CallbackQuery.edit_message_text(_["song_10"])
        finally:
            os.remove(filename)

    os.remove(thumb_image_path)
