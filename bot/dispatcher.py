from asgiref.sync import sync_to_async
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import filters, ContextTypes, Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler

from .translation import get_text as t
from .models import Customer, Product, Order

REGISTER_PHONE, REGISTER_LOCATION, ORDER, ORDER_AMOUNT, ORDER_CONFIRM = range(5)

MAX_COLUMN_COUNT = 4


async def get_products():
    products_raw = await sync_to_async(Product.objects.all)()
    products = await sync_to_async(list)(products_raw)
    return products, len(products) 

def make_product_msg(product):
    return f"{product.name} \n\n {product.description}"

def re_arrange(arr, max_count):
    result = []
    for i in range(0, len(arr), max_count):
        result.append(arr[i:i + max_count])
    return result

def make_product_reply_markup(products, count):
    keyboard = []

    for product in products:
        keyboard.append(
            InlineKeyboardButton(
                product.name,
                callback_data=product.id,
            )
        )

    keyboard = re_arrange(keyboard, MAX_COLUMN_COUNT)

    return InlineKeyboardMarkup(keyboard)




# def make_product_reply_markup(index, count):
#     no_data_keyboard = InlineKeyboardButton("❌", callback_data="-1")
#     prev_keyboard = InlineKeyboardButton("⬅️ Oldingi", callback_data="prev") if index > 0 else no_data_keyboard
#     next_keyboard = InlineKeyboardButton("Keyingi ➡️", callback_data="next") if index < count-1 else no_data_keyboard
#     select_keyboard = InlineKeyboardButton("📥 Tanlash", callback_data="select")
#     keyboard = [
#         [prev_keyboard, select_keyboard, next_keyboard],
#     ]
#     return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # language_code = update.message.from_user.language_code
    user_tg_id = update.message.from_user.id
    is_registered_user = await sync_to_async(Customer.objects.filter(telegram_id=user_tg_id).exists)()

    #  check if user previously registered
    if not is_registered_user:
        contact_button = KeyboardButton(text="please share your phone number", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("not registered", reply_markup=reply_markup)
        return REGISTER_PHONE

    reply_keyboard = [
        [t('order'), t('my_orders')],
        [t('contact_operator'), t('settings')],
    ]
    await update.message.reply_text(
        t('intro'),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    curr_product_index = context.user_data.get("curr_product_index", 0)
    products, count = await get_products()
    
    image_path = 'media/overview.jpg'
    await update.message.reply_photo(
        photo=open(image_path, 'rb'),
        caption="this is caption",
        reply_markup=make_product_reply_markup(products, count)
    )
    # await update.message.reply_text(
    #     make_product_msg(products[curr_product_index]),
    #     reply_markup=make_product_reply_markup(curr_product_index, count)
    # )
    return ORDER_AMOUNT


async def order_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # print("query****************")
    # print(update.callback_query)

    query = update.callback_query
    curr_product_index = context.user_data.get("curr_product_index", 0)
    products, count = await get_products()

    await query.answer()

    # if user selects the product, next step is asking amount
    if query.data == 'select':
        context.user_data['current_product_id'] = products[curr_product_index].id
        await query.edit_message_text("amount?")
        return

    if query.data == 'next':
        curr_product_index += 1
    elif query.data == 'prev':
        curr_product_index -= 1

    context.user_data['curr_product_index'] = curr_product_index


    await query.edit_message_text(
        make_product_msg(products[curr_product_index]),
        reply_markup=make_product_reply_markup(curr_product_index, count)
    )


async def order_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = int(update.message.text)
        context.user_data['product_amount'] = amount
    except ValueError:
        await update.message.reply_text("wrong input!!")
        return ORDER_AMOUNT
    
    reply_markup = [
        [M_ORDER_CONFIRM],
        [M_ORDER_CANCEL],
    ]

    await update.message.reply_text(
        "amout: " + update.message.text,
        reply_markup=ReplyKeyboardMarkup(reply_markup, resize_keyboard=True)    
    )
    return ORDER_CONFIRM


async def order_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get customer id
    user_tg_id = update.message.from_user.id
    customer = await sync_to_async(
        Customer.objects.get
    )(
        telegram_id=user_tg_id
    )
    
    
    product_id = context.user_data['current_product_id']
    product_amount = context.user_data['product_amount']

    await sync_to_async(
        Order.objects.create
    )(
        customer=customer,
        product_id=product_id,
        amount=product_amount,
    )

    await update.message.reply_text("you order successfully confirmed.")
    return ConversationHandler.END


async def register_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('-- contact: ')
    user_tg_id = update.message.from_user.id
    if not user_tg_id == update.message.contact.user_id:
        await update.message.reply_text("this is not yours!")
        return REGISTER_PHONE
    
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
    
    return REGISTER_LOCATION


async def register_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("location: ")
    print(update.message.location.latitude, update.message.location.longitude)
    return ConversationHandler.END


def setup_application(app: Application):

    app.add_handler(CommandHandler('start', start))

    order_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^({t('order')})$'), order)
        ],
        states={
            # ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
            REGISTER_PHONE: [MessageHandler(filters.CONTACT & ~filters.COMMAND, register_phone)],
            REGISTER_LOCATION: [MessageHandler(filters.LOCATION & ~filters.COMMAND, register_location)],
            ORDER_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_amount)],
            ORDER_CONFIRM: [MessageHandler(filters.Regex(f'^({t('confirm_order')})$'), order_confirm)],
        },
        fallbacks=[]
    )
    app.add_handler(order_conv_handler)
    app.add_handler(CallbackQueryHandler(order_button))

    return app
