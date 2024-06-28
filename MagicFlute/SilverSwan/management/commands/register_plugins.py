from django.core.management.base import BaseCommand
from SilverSwan.register_plugins import register_plugins

class Command(BaseCommand):
    help = 'Register all plugins'

    def handle(self, *args, **options):
        register_plugins()
        if options['verbosity'] > 0:
            self.stdout.write(self.style.SUCCESS('Successfully registered plugins'))