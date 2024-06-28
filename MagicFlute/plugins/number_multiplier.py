from SilverSwan.base_plugin import BasePlugin

class NumberMultiplier(BasePlugin):
    """
    Multiplies input 1 by input 2.
    """
    def __init__(self, name, description):
        super().__init__(name, description)
        self.progress_value = 0
        self.total_steps = 1

    def execute(self, input_data):
        number1 = input_data.get('number1')
        number2 = input_data.get('number2')

        if number1 is None or number2 is None:
            raise ValueError("Both number1 and number2 must be provided.")

        try:
            result = float(number1) * float(number2)
            return {'result': result}
        except (TypeError, ValueError):
            raise ValueError("Invalid input values. Please provide valid numbers.")

    def get_config_schema(self):
        return {
            'plugin_type': 'computational',
            'inputs': [
                {'name': 'number1', 'type': 'float', 'description': 'Input number one'},
                {'name': 'number2', 'type': 'float', 'description': 'Input number two'}
            ],
            'outputs': [
                {'name': 'result', 'type': 'float', 'description': 'Multiplication result'}
            ]
        }

    def log_success(self, workflow_instance, result):
        self.progress_value = self.total_steps
        workflow_instance.log_plugin_execution(
            plugin_name=self.name,
            success=True,
            failure_reason=None,
            output=result
        )

    def log_failure(self, workflow_instance, failure_reason):
        self.progress_value = self.total_steps
        workflow_instance.log_plugin_execution(
            plugin_name=self.name,
            success=False,
            failure_reason=failure_reason,
            output=None
        )