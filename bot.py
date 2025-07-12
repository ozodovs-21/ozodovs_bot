import os
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import requests

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 Video va 🎵 audio yuklovchi botga xush kelibsiz! Link yoki musiqa nomini yuboring.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "tiktok.com" in url or "youtube.com" in url or "youtu.be" in url or "instagram.com" in url:
        await update.message.reply_text("⏬ Yuklab olinmoqda, iltimos kuting...")
        ydl_opts = {
            'outtmpl': 'downloaded.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for ext in ['mp4', 'mkv', 'webm']:
                filename = f"downloaded.{ext}"
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        await update.message.reply_video(f)
                    os.remove(filename)
                    return
        except Exception as e:
            await update.message.reply_text(f"❌ Xatolik: {e}")
    else:
        await update.message.reply_text("🔗 Link noto‘g‘ri yoki qo‘llab-quvvatlanmaydi.")

async def text_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not any(x in query for x in ['http', '.com']):
        await update.message.reply_text(f"🔍 Musiqa nomi bo‘yicha qidirilmoqda: '{query}' (faqat demo).")
        # Real implementation would use APIs like YouTube Data API
    else:
        await download_video(update, context)

app = ApplicationBuilder().token("7989565357:AAFO-7Y75KmERq2abyDgjfaHjohGvgmh-6Y").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_search))

app.run_polling()
