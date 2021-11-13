from django.db import models
from picklefield.fields import PickledObjectField

# Create your models here.
class UploadedImage(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()

class Places(models.Model): 
    name = models.CharField(max_length = 30)
    image_url = models.CharField(max_length = 100)
    rgb = PickledObjectField()
    image = models.ImageField(default = '북촌.jpeg' )
    location = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Foot_Traffic(models.Model):
    place = models.ForeignKey(Places , on_delete=models.CASCADE)
    traffic_level = models.FloatField()
    date = models.DateField()

    

