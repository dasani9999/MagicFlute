import os
import importlib
from django.conf import settings
from .models import Plugin
from .base_plugin import BasePlugin

def register_plugins():
    plugins_dir = os.path.join(settings.BASE_DIR, 'plugins')
    plugin_files = [f for f in os.listdir(plugins_dir) if f.endswith('.py')]

    for plugin_file in plugin_files:
        module_name = os.path.splitext(plugin_file)[0]
        module_path = f'plugins.{module_name}'
        module = importlib.import_module(module_path)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr.__name__ != 'BasePlugin':
                plugin_instance = attr(name=attr_name, description=attr.__doc__ or 'No description provided')
                plugin_name = plugin_instance.name
                plugin_description = plugin_instance.description
                plugin_class_name = f'{module_path}.{attr.__name__}'
                plugin_type = plugin_instance.get_config_schema().get('plugin_type', 'unknown')  # Get plugin type

                # Check if the plugin already exists in the database
                plugin, created = Plugin.objects.update_or_create(
                    name=plugin_name,
                    defaults={
                        'description': plugin_description,
                        'class_name': plugin_class_name,
                        'plugin_type': plugin_type  # Add plugin type
                    }
                )

                if created:
                    print(f"Created new plugin: {plugin_name}")
                else:
                    print(f"Updated existing plugin: {plugin_name}")

# Call the register_plugins function to register the plugins
register_plugins()
