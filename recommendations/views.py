from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage
# Create your views here.

def homePageView(request):
    if request.method == "POST":
        uploadedimage_instance = UploadedImage()

        #save image into the system 
        img = request.FILES['image']
        img_name = img.name
        fs = FileSystemStorage()
        fs.save(img_name , img)

        #also save image to a database
        uploadedimage_instance.image = img
        uploadedimage_instance.name = img_name
        uploadedimage_instance.save()
    return render(request,'home.html')