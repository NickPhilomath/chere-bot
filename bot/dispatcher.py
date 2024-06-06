from asgiref.sync import sync_to_async
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import filters, ContextTypes, Application, CommandHandler, MessageHandler, ConversationHandler

from customers.models import Customer

PHONE = range(1)

M_WELCOME = 'Welcome to our Company'
M_CHOOSE_LANGUAGE = 'Please choose a language'
M_ORDER = '🚛 Buyurtma qilish'
M_ABOUT_COMPANY = '🏢 Kompaniya haqida'
M_CONTACT = "📞 Operator bilan bog'lanish"
M_SETTINGS = '⚙️ Settings'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_tg_id = update.message.from_user.id
    language_code = update.message.from_user.language_code


    reply_keyboard = [
        [M_ORDER, M_CONTACT],
        [M_ABOUT_COMPANY, M_SETTINGS],
    ]
    await update.message.reply_text(
        M_WELCOME,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_tg_id = update.message.from_user.id
    is_registered_user = await sync_to_async(Customer.objects.filter(telegram_id=user_tg_id).exists)()

    if not is_registered_user:
        contact_button = KeyboardButton(text="please share your phone number", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("not registered", reply_markup=reply_markup)
        return PHONE
    await update.message.reply_text("registered")
    return ConversationHandler.END


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('-- contact: ')
    print(update)
    user_tg_id = update.message.from_user.id
    if not user_tg_id == update.message.contact.user_id:
        await update.message.reply_text("this is not yours!")
        return PHONE
    await update.message.reply_text(f'your phone number: {update.message.contact.phone_number}')
    return ConversationHandler.END


def setup_application(app: Application):

    app.add_handler(CommandHandler('start', start))

    order_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^({M_ORDER})$'), order)
        ],
        states={
            PHONE: [MessageHandler(filters.CONTACT & ~filters.COMMAND, phone)]
        },
        fallbacks=[]
    )
    app.add_handler(order_conv_handler)

    return app
