import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from app import run_agent 

load_dotenv()

# Pastikan TELEGRAM_BOT_TOKEN ada di .env
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya adalah CSBot. Ketik pertanyaanmu untuk mendapatkan jawaban.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    # Panggil run_agent dari app.py untuk memproses pertanyaan
    response = run_agent(user_input)
    await update.message.reply_text(response)

def main():
    # Buat application/instance bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handler untuk command /start
    app.add_handler(CommandHandler("start", start))

    # Handler untuk pesan teks
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
