class BasePlugin:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self, input_data):
        raise NotImplementedError("Subclasses must implement the execute method.")

    def get_config_schema(self):
        raise NotImplementedError("Subclasses must implement the get_config_schema method.")