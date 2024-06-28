from SilverSwan.base_plugin import BasePlugin

class NumberAdderSubtractor(BasePlugin):
    """
    Subtracts number3 from number1 and adds number2 to number4.
    """
    def __init__(self, name, description):
        super().__init__(name, description)
        self.progress_value = 0
        self.total_steps = 1

    def execute(self, input_data):
        number1 = input_data.get('number1')
        number2 = input_data.get('number2')
        number3 = input_data.get('number3')
        number4 = input_data.get('number4')

        if number1 is None or number2 is None or number3 is None or number4 is None:
            raise ValueError("All four inputs must be provided.")

        try:
            result1 = float(number1) - float(number3)
            result2 = float(number2) + float(number4)
            return {'result1': result1, 'result2': result2}
        except (TypeError, ValueError):
            raise ValueError("Invalid input values. Please provide valid numbers.")

    def get_config_schema(self):
        return {
            'plugin_type': 'computational',
            'inputs': [
                {'name': 'number1', 'type': 'float', 'description': 'Input number one'},
                {'name': 'number2', 'type': 'float', 'description': 'Input number two'},
                {'name': 'number3', 'type': 'float', 'description': 'Input number three'},
                {'name': 'number4', 'type': 'float', 'description': 'Input number four'}
            ],
            'outputs': [
                {'name': 'result1', 'type': 'float', 'description': 'Subtraction result'},
                {'name': 'result2', 'type': 'float', 'description': 'Addition result'}
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
