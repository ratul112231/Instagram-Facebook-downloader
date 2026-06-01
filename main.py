import os
import time
import base64
import threading
from flask import Flask
import telebot
from telebot import types
import yt_dlp

# =========================
# CONFIG
# =========================

BOT_TOKEN = "8864648929:AAGY5_j3a0AGj2oQsRHVyVQ75tNfk9qJtk0"

bot = telebot.TeleBot(BOT_TOKEN)

# Hidden Links (Base64 Encoded)
YOUTUBE_LINK = base64.b64decode(
    "aHR0cHM6Ly95b3V0dWJlLmNvbS9AYmxhY2trbm93bGVkZ2VfMTkwP3NpPTlFd2tNUEdiLWxIUnpaZHE="
).decode()

SUPPORT_LINK = base64.b64decode(
    "aHR0cHM6Ly90Lm1lL0JMQUNLX0tub3dsZWRnZV8xOTA="
).decode()

# =========================
# FLASK SERVER
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running Successfully"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    threading.Thread(target=run_flask).start()

# =========================
# START COMMAND
# =========================

@bot.message_handler(commands=['start'])
def start_command(message):

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(
        "📢 SUBSCRIBE CHANNEL",
        url=https://t.me/G8rSWrAFzo1YzY1
    )

    btn2 = types.InlineKeyboardButton(
        "🎓 ALL TUTORIALS",
        url=https://t.me/G8rSWrAFzo1YzY1
    )

    btn3 = types.InlineKeyboardButton(
        "👤 CONTACT OWNER",
        url=https://t.me/G8rSWrAFzo1YzY1
    )

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    text = f"""
✨ Welcome to Premium Video Downloader Bot

📥 Download Instagram Reels & Facebook Videos
⚡ Fast Processing
🚀 Professional Downloader

Powered By:
@BLACK_KNOWLEDGE_190
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

# =========================
# DOWNLOAD FUNCTION
# =========================

def download_video(url):

    filename = f"video_{int(time.time())}.mp4"

    ydl_opts = {
        "outtmpl": filename,
        "format": "mp4/best"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename

# =========================
# LINK HANDLER
# =========================

@bot.message_handler(func=lambda msg: True)
def video_handler(message):

    url = message.text.strip()

    status = bot.reply_to(
        message,
        "🔍 Analyzing Link..."
    )

    try:
        time.sleep(1)

        bot.edit_message_text(
            "📥 Downloading... (50%)",
            chat_id=status.chat.id,
            message_id=status.message_id
        )

        file_path = download_video(url)

        time.sleep(1)

        bot.edit_message_text(
            "📤 Uploading... (100%)",
            chat_id=status.chat.id,
            message_id=status.message_id
        )

        with open(file_path, "rb") as video:

            bot.send_video(
                message.chat.id,
                video,
                caption=(
                    "Downloaded Successfully!\n"
                    "Power by: @BLACK_KNOWLEDGE_190"
                )
            )

        # Cleanup
        os.remove(file_path)

        bot.delete_message(
            status.chat.id,
            status.message_id
        )

    except Exception as e:

        bot.edit_message_text(
            f"❌ Error:\n{e}",
            chat_id=status.chat.id,
            message_id=status.message_id
        )

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    keep_alive()

    print("Bot Started")

    bot.infinity_polling(skip_pending=True)
