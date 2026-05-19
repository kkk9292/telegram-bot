import os
os.system("pip install python-telegram-bot")
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

CHANNEL_ID = "@karrar_eg"
FILE_ID = "BQACAgIAAxkBAAMlagtIgLEW0xzAmQa2DUNMus6ID2AAAo6lAALOG1hI0pO97qhbuVs7BA"

BOT_TOKEN = "8919817428:AAEprBUcU3TCbyLkXUdKIFQ_pONPR2JKm2Iا"


async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "📢 اشترك بالقناة",
            url="https://t.me/karrar_eg"
        )],
        [InlineKeyboardButton(
            "✅ تحقق من الاشتراك",
            callback_data="check_sub"
        )]
    ]

    await update.message.reply_text(
        "👋 اشترك بالقناة أولاً ثم اضغط تحقق من الاشتراك",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    if query.data == "check_sub":
        if await check_subscription(context.bot, user_id):

            await context.bot.send_document(
                chat_id=user_id,
                document=FILE_ID,
                caption="📄 شكراً لاشتراككم بالقناة مع تمنياتي لكم بالنجاح"
            )

        else:
            await query.answer(
                "❌ عذراً أنت غير مشترك بالقناة",
                show_alert=True
            )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("البوت يعمل...")
app.run_polling()
