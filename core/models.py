from django.db import models

# Create your models here.

class ConfigurationModel(models.Model):
    audio_file = models.FileField(upload_to='audio_file')
    
    def __str__(self):
        return str(self.id)