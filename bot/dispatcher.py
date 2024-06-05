from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, ConversationHandler

LANGUAGE = range(1)

M_WELCOME = 'Welcome to our Company'
M_CHOOSE_LANGUAGE = 'Please choose a language'
M_ABOUT_COMPANY = '🏢 Kompaniya haqida'
M_ORDER = '🚛 Buyurtma qilish'
M_CONTACT = "📞 Operator bilan bog'lanish"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('-- Start: ', update.message.from_user)
    language_code = update.message.from_user.language_code

    reply_keyboard = [
        [M_ABOUT_COMPANY],
        [M_ORDER],
        [M_CONTACT],
    ]
    await update.message.reply_text(
        M_WELCOME,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return LANGUAGE


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return 0



def setup_application(app: Application):

    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # LANGUAGE: MessageHandler()
        },
        fallbacks=[]
    )
    app.add_handler(main_conv_handler)

    return app
