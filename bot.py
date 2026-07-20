import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8547710382:AAFYAU3gS-60z6LE--NO79l-N9nYeos7Kn4"
ADMIN_ID = 1170411845  # غيّره لمعرفك

logging.basicConfig(level=logging.INFO)

# ===== أوامر البوت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 إحصائيات", callback_data="stats")],
        [InlineKeyboardButton("📢 إرسال جماعي", callback_data="broadcast")],
        [InlineKeyboardButton("💀 حذف مجموعة", callback_data="delete_group")],
    ]
    await update.message.reply_text(
        "🔥 الظل المبرمج جاهز. اختر مهمتك:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "stats":
        await query.edit_message_text("📊 عدد المستخدمين: 0")
    elif query.data == "broadcast":
        await query.edit_message_text("📢 أرسل الرسالة:")
    elif query.data == "delete_group":
        await query.edit_message_text("💀 تم حذف المجموعة.")

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ استخدم: /spam <عدد> <نص>")
        return
    try:
        count = int(context.args[0])
        text = " ".join(context.args[1:])
        for _ in range(count):
            await update.message.reply_text(text)
    except:
        await update.message.reply_text("❌ خطأ في الصيغة.")

async def delete_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.message.reply_to_message.delete()
        await update.message.reply_text("🗑️ تم الحذف.")
    else:
        await update.message.reply_text("⚠️ ارد على الرسالة.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.message.chat.ban_member(user.id)
        await update.message.reply_text(f"🚫 تم حظر {user.first_name}.")
    else:
        await update.message.reply_text("⚠️ ارد على العضو.")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            user_id = int(context.args[0])
            await update.message.chat.unban_member(user_id)
            await update.message.reply_text(f"✅ تم فك الحظر عن {user_id}.")
        except:
            await update.message.reply_text("❌ معرف غير صحيح.")
    else:
        await update.message.reply_text("⚠️ استخدم: /unban <id>")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.message.chat.restrict_member(user.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"🔇 تم كتم {user.first_name}.")
    else:
        await update.message.reply_text("⚠️ ارد على العضو.")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.message.chat.restrict_member(user.id, ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"🔊 تم فك الكتم عن {user.first_name}.")
    else:
        await update.message.reply_text("⚠️ ارد على العضو.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    await update.message.reply_text(
        f"📌 الاسم: {user.first_name}\n"
        f"🆔 المعرف: `{user.id}`\n"
        f"👤 اليوزر: @{user.username if user.username else 'لا يوجد'}"
    )

async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 معرف المجموعة: `{update.message.chat.id}`")

async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 وداعًا.")
    await update.message.chat.leave()

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("🔄 إعادة تشغيل...")
        os._exit(0)
    else:
        await update.message.reply_text("⛔ غير مصرح.")

# ===== تشغيل Webhook =====
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("spam", spam))
    app.add_handler(CommandHandler("delete", delete_msg))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("chatid", chatid))
    app.add_handler(CommandHandler("leave", leave))
    app.add_handler(CommandHandler("restart", restart))

    # وضع Webhook (مهم لـ Render)
    PORT = int(os.environ.get("PORT", 8443))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://ab-dr25.onrender.com/{TOKEN}"
    )

if __name__ == "__main__":
    main()    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
