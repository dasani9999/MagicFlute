import json, pdb
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.utils.module_loading import import_string as locate
from .models import Plugin
# Create your views here.


def main_view(request):
    plugins = Plugin.objects.all()
    return render(request, 'main.html', {'plugins': plugins})


def get_plugin_config(request, plugin_id):
    plugin = get_object_or_404(Plugin, id=plugin_id)
    plugin_class = locate(plugin.class_name)
    config_schema = plugin_class(name=plugin.name, description=plugin.description).get_config_schema()
    return JsonResponse(config_schema)

@csrf_exempt
def execute_plugin(request, plugin_id):
    plugin = get_object_or_404(Plugin, id=plugin_id)
    plugin_class = locate(plugin.class_name)
    plugin_instance = plugin_class(name=plugin.name, description=plugin.description)

    input_data = request.POST.dict()
    instance_id = input_data.get('instance_id')

    try:
        output = plugin_instance.execute(input_data)
        return JsonResponse({'output': output})
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def execute_workflow(request):
    workflow_data = json.loads(request.body)['workflow']
    plugin_results = {}

    def generate_updates():
        for index, plugin_data in enumerate(workflow_data):
            plugin_id = plugin_data['pluginId']
            instance_id = plugin_data['instanceId']
            plugin_type = plugin_data['pluginType']
            inputs = plugin_data['inputs']

            # Process the plugin
            plugin_result = process_plugin(plugin_id, plugin_type, inputs, plugin_results)
            plugin_results[instance_id] = plugin_result

            # Prepare update data
            update_data = {
                'pluginId': plugin_id,
                'instanceId': instance_id,
                'status': 'success',
                'message': f'Plugin {plugin_id} processed successfully',
                'result': plugin_result,
                'progress': ((index + 1) / len(workflow_data)) * 100
            }

            yield json.dumps(update_data) + '\n'

    return StreamingHttpResponse(generate_updates(), content_type='application/json')

def process_plugin(plugin_id, plugin_type, inputs, plugin_results):
    plugin = get_object_or_404(Plugin, id=plugin_id)
    plugin_class = locate(plugin.class_name)
    plugin_instance = plugin_class(name=plugin.name, description=plugin.description)

    # Prepare input data
    input_data = {}
    for input_item in inputs:
        if isinstance(input_item['value'], dict) and 'linkedInstanceId' in input_item['value']:
            # This is a linked input, get the value from the previous plugin result
            linked_instance_id = input_item['value']['linkedInstanceId']
            linked_output = input_item['value']['linkedOutput']
            input_data[input_item['name']] = plugin_results[linked_instance_id][linked_output]
        else:
            input_data[input_item['name']] = input_item['value']

    # Execute the plugin
    if plugin_type == 'variable_storage':
        return input_data
    else:
        return plugin_instance.execute(input_data)

