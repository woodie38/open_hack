from django.contrib import admin
from .models import UploadedImage, Places, Foot_Traffic


# Register your models here.
admin.site.register(UploadedImage)
admin.site.register(Places)
admin.site.register(Foot_Traffic)