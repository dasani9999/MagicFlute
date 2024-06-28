from django.db import models

class Plugin(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class_name = models.CharField(max_length=200)
    plugin_type = models.CharField(max_length=50, default='unknown')  # Add this field

    def __str__(self):
        return self.name