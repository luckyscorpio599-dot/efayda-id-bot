import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from pdf_processor import extract_pdf_data, extract_images_from_pdf
from id_generator import generate_id_image

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send your EFAYDA PDF and I will generate your ID.")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    await file.download_to_drive("incoming.pdf")

    await update.message.reply_text("Processing your PDF…")

    data = extract_pdf_data("incoming.pdf")
    photo, qr, barcode = extract_images_from_pdf("incoming.pdf")
    final = generate_id_image(data, photo, qr, barcode)

    await update.message.reply_photo(photo=open(final, "rb"))
    await update.message.reply_text("✅ Your ID is ready!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.run_polling()

if __name__ == "__main__":
    main()
