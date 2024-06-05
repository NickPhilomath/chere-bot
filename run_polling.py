import os, django
from telegram import Update
from telegram.ext import Application

from chere.settings import BOT_TOKEN
from bot.dispatcher import setup_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chere.settings')
django.setup()

def run_polling(tg_token: str = BOT_TOKEN):
    print("-- Aplication started.")
    # print("-- Using token: ", BOT_TOKEN)

    application = Application.builder().token(tg_token).build()
    
    setup_application(application)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    run_polling()