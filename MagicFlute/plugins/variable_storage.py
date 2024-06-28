from SilverSwan.base_plugin import BasePlugin

class VariableStorage(BasePlugin):
    """
    A variable input/storage plugin that allows dynamic addition of inputs and their associated outputs.
    """
    def __init__(self, name, description):
        super().__init__(name, description)

    def execute(self, input_data):
        # This plugin doesn't process data, it just stores it
        return input_data

    def get_config_schema(self):
        return {
            'plugin_type': 'variable_storage',
            'inputs': [
                {'name': 'variable_1', 'type': 'dynamic', 'description': 'Variable 1'}
            ],
            'outputs': [
                {'name': 'variable_1', 'type': 'dynamic', 'description': 'Variable 1 Output'}
            ]
        }