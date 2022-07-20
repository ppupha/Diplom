from django.db import models

# Create your models here.

class TestLight(models.Model):
    name = models.CharField(max_length= 100, default='***')
    isOn = models.BooleanField(default = False)

    def __str__(self):
        return self.name

