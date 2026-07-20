import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ===== تنشيط السجلات =====
logging.basicConfig(level=logging.INFO)

# ===== التوكن من متغيرات البيئة =====
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("ضع التوكن في متغير البيئة TOKEN")

# ===== أوامر البوت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 إحصائيات", callback_data="stats")],
        [InlineKeyboardButton("📢 إرسال جماعي", callback_data="broadcast")],
    ]
    await update.message.reply_text(
        "🔥 أنا بوتك الشرير، اختر أمرًا:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "stats":
        await query.edit_message_text("📊 عدد المستخدمين: 0 (لكن بإمكانك إضافة قاعدة بيانات).")
    elif query.data == "broadcast":
        await query.edit_message_text("📢 أرسل الرسالة التي تريد نشرها.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📨 قلت: {update.message.text}")

# ===== تشغيل البوت =====
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
