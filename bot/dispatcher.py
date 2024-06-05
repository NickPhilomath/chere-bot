from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import filters, ContextTypes, Application, CommandHandler, MessageHandler, ConversationHandler

from customers.models import Customer

LANGUAGE = range(1)

M_WELCOME = 'Welcome to our Company'
M_CHOOSE_LANGUAGE = 'Please choose a language'
M_ORDER = '🚛 Buyurtma qilish'
M_ABOUT_COMPANY = '🏢 Kompaniya haqida'
M_CONTACT = "📞 Operator bilan bog'lanish"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('-- Start: ', update)
    user_tg_id = update.message.from_user.id
    language_code = update.message.from_user.language_code

    is_registered_user = Customer.objects.filter(telegram_id=user_tg_id).exists()

    if is_registered_user:
        print('registered')
    else:
        print('NOT registered')


    reply_keyboard = [
        [M_ORDER],
        [M_ABOUT_COMPANY],
        [M_CONTACT],
    ]
    await update.message.reply_text(
        M_WELCOME,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return LANGUAGE


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("order section")
    return ConversationHandler.END



def setup_application(app: Application):

    app.add_handler(CommandHandler('start', start))

    order_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^({M_ORDER})$'), order)
        ],
        states={
            # LANGUAGE: MessageHandler(filters.TEXT, language)
        },
        fallbacks=[]
    )
    app.add_handler(order_conv_handler)

    return app
