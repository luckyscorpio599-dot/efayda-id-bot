import os
import threading
import http.server
import socketserver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from pdf_processor import extract_pdf_data, extract_images_from_pdf
from id_generator import generate_id_image

# --- 1. THE WEB SERVER (To stay alive on Render Free Tier) ---
def run_health_server():
    # Render automatically sets the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    # This keeps the 'Web Service' active
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Health server running on port {port}")
        httpd.serve_forever()

# Start the health server in a background thread
threading.Thread(target=run_health_server, daemon=True).start()

# --- 2. YOUR BOT CODE ---
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send your EFAYDA PDF and I will generate your ID.")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.document.get_file()
        await file.download_to_drive("incoming.pdf")

        await update.message.reply_text("Processing your PDF...")

        data = extract_pdf_data("incoming.pdf")
        photo, qr, barcode = extract_images_from_pdf("incoming.pdf")
        final = generate_id_image(data, photo, qr, barcode)

        with open(final, "rb") as photo_file:
            await update.message.reply_photo(photo=photo_file)
        await update.message.reply_text("✅ Your ID is ready!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_TOKEN environment variable is not set!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    
    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
