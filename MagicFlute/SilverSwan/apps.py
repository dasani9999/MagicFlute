from django.apps import AppConfig
import sys
from django.core.management import call_command

class SilverswanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SilverSwan'

    def ready(self):
        if 'runserver' in sys.argv:
            # Use the Django system check framework to register plugins
            from django.core.checks import register, Tags
            from django.core.checks import Warning

            @register(Tags.models)
            def check_register_plugins(app_configs, **kwargs):
                try:
                    call_command('register_plugins', verbosity=0)
                except Exception as e:
                    return [Warning(
                        f'Failed to register plugins: {str(e)}',
                        hint='Check your plugin registration process.',
                        obj=self,
                    )]
                return []