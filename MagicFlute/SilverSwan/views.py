import json, pdb
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    workflow_data = json.loads(request.body)

    # Extract the plugin instances and their connections from the workflow data
    # ...

    # Execute the plugins in the correct order based on the connections
    # Pass the output of one plugin as the input to the next plugin
    # ...

    # Collect the output of each plugin instance
    # ...

    return JsonResponse({'output': workflow_output})

