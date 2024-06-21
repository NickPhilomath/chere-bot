from telegram.ext import Application
from telegram import Update
from django.core.management.base import BaseCommand, CommandError

from chere.settings import BOT_TOKEN
from bot.dispatcher import setup_application


class Command(BaseCommand):
    help = 'Describe your command here'

    # def add_arguments(self, parser):
    #     # Define command-line arguments here
    #     parser.add_argument('arg1', type=str, help='Argument 1 description')
    #     parser.add_argument('--optional_arg', type=int, help='Optional argument description', default=42)

    def handle(self, *args, **options):
        print("-- Aplication started.")
        # print("-- Using token: ", BOT_TOKEN)
        application = Application.builder().token(BOT_TOKEN).build()
        setup_application(application)
        application.run_polling(allowed_updates=Update.ALL_TYPES)