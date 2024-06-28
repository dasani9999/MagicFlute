from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('plugins/<int:plugin_id>/config/', views.get_plugin_config, name='get_plugin_config'),
    path('plugins/<int:plugin_id>/execute/', views.execute_plugin, name='execute_plugin'),
    path('execute-workflow/', views.execute_workflow, name='execute_workflow'),
]