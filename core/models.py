from django.db import models

# Create your models here.

class ConfigurationModel(models.Model):
    audio_file = models.FileField(upload_to='audio_file')
    
    def __str__(self):
        return str(self.id)
    
    
class Ips(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=222)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name