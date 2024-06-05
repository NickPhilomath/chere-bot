from django.core.management.base import BaseCommand, CommandError

from run_polling import run_polling

class Command(BaseCommand):
    help = 'Describe your command here'

    # def add_arguments(self, parser):
    #     # Define command-line arguments here
    #     parser.add_argument('arg1', type=str, help='Argument 1 description')
    #     parser.add_argument('--optional_arg', type=int, help='Optional argument description', default=42)

    def handle(self, *args, **options):
        run_polling()
        # arg1 = options['arg1']
        # optional_arg = options['optional_arg']

        # # Implement your custom command logic here
        # self.stdout.write(self.style.SUCCESS(f'Argument 1: {arg1}'))
        # self.stdout.write(self.style.SUCCESS(f'Optional Argument: {optional_arg}'))

        # You can raise a CommandError to indicate something went wrong
        # if some_condition:
        #     raise CommandError('An error occurred')