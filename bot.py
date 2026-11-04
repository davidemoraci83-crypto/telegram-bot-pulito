import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from duckduckgo_search import DDGS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def search_and_send_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    query = update.message.text.strip()
    await update.message.reply_text(f"⏳ Cerco immagini per: {query}...")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))

        if results:
            image_url = results['image']
            await update.message.reply_photo(photo=image_url)
        else:
            await update.message.reply_text("❌ Nessuna immagine trovata.")
    except Exception as e:
        logger.error(f"Errore durante la ricerca: {e}")
        await update.message.reply_text("⚠️ Si è verificato un errore durante la ricerca.")

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        logger.error("Errore: Token del bot Telegram non trovato!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_and_send_image))

    logger.info("Bot avviato e in ascolto...")
    application.run_polling()

if __name__ == '__main__':
    main()
