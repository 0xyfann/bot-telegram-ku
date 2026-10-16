import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

# Mengambil token dari sistem
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# Menyiapkan Gemini
client = genai.Client(api_key=GEMINI_KEY)

async def mulai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya bot AI kamu. Mau ngobrol apa hari ini?")

async def balas_pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan_user = update.message.text
    
    # Menampilkan tulisan "typing..." (mengetik) di Telegram
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Mengirim pesan ke Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=pesan_user,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Waduh, botnya lagi pusing. Coba lagi ya!")

if __name__ == '__main__':
    # Menjalankan bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", mulai))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), balas_pesan))
    
    print("Bot sedang berjalan...")
    app.run_polling()
  
