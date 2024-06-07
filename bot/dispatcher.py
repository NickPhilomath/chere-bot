from asgiref.sync import sync_to_async
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ContextTypes, Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler

from .models import Customer, Product

PHONE = range(1)

M_WELCOME = 'Welcome to our Company'
M_CHOOSE_LANGUAGE = 'Please choose a language'
M_ORDER = '🚛 Buyurtma qilish'
M_ABOUT_COMPANY = '🏢 Kompaniya haqida'
M_CONTACT = "📞 Operator bilan bog'lanish"
M_SETTINGS = '⚙️ Settings'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    

    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Oldingi", callback_data="prev"),
            InlineKeyboardButton("📥 Tanlash", callback_data="select"),
            InlineKeyboardButton("Keyingi ➡️", callback_data="next"),
        ],
    ]

    current_product_index = context.user_data.get("current_product", 0)
    
    products_raw = await sync_to_async(Product.objects.all)()
    products = await sync_to_async(list)(products_raw)

    current_product = products[current_product_index]


    print("products: *****************")
    print(products)
    # # print(products)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"{current_product.name} \n\n {current_product.description}", 
        reply_markup=reply_markup
    )
    return ConversationHandler.END


async def order_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    print("query****************")
    print(query)

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('-- contact: ')
    user_tg_id = update.message.from_user.id
    if not user_tg_id == update.message.contact.user_id:
        await update.message.reply_text("this is not yours!")
        return PHONE
    
    # register new user
    language_code = update.message.from_user.language_code
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    await sync_to_async(
        Customer.objects.create
    )(
        telegram_id = user_tg_id,
        name = f'{first_name} {last_name}',
        phone = update.message.contact.phone_number,
        language = language_code if language_code in ['en', 'uz', 'ru'] else 'uz',
    )
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
    app.add_handler(CallbackQueryHandler(order_button))

    return app
