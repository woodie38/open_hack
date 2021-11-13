from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db.models import Avg
from .models import Foot_Traffic, UploadedImage, Places



from . import recommend
import numpy as np
import pandas as pd

#import recommend
# Create your views here.

def homePageView(request):
    if request.method == "POST":
        uploadedimage_instance = UploadedImage()

        #save image into the system 
        img = request.FILES['image']
        img_name = img.name
        

        #save image to a database
        uploadedimage_instance.image = img
        uploadedimage_instance.name = img_name
        uploadedimage_instance.save()

        img = 'static/media/images/'+img.name
        all_places = Places.objects.all()
        
        #here, use destination API to search for number of ppl 
        similarity_dict_t10 = recommend.get_top_10_similarity(img,all_places)

        traffic_dict = {}
        for name in similarity_dict_t10.keys():
            
            foot_traffic_objects = Foot_Traffic.objects.filter(place__name = name)
            mean_traffic = foot_traffic_objects.aggregate(Avg('traffic_level'))
            mean_traffic = mean_traffic['traffic_level__avg']
            traffic_dict[name] = mean_traffic
            
        
        top_three = list(sorted(traffic_dict.items(), key=lambda item: item[1]))[:3]
        three_names = []

        for i in range(len(top_three)):
            three_names.append(top_three[i][0])
        


        place_list = []
        for name in three_names: 
            place = Places.objects.get(name = name)
            place_list.append(place)
        print(place_list)

        return render(request,'home.html', {'three_places' : place_list})

        


        # get the bottom3 


        #show the three here 
        #render on template
        


    return render(request,'home.html')




"""
#compare all similarity scores
        similiarty_list = []
        for place in all_places: 
            matrix_B = place.rgb 
            name = place.name 
            url = place.url
            

            similarity_rate = euclid_dist(matrix_A,matrix_B)
            similarity_dict = {'name' : name , 'similarity_rate' : similarity_rate }
            similiarty_list.append(similarity_dict)
        
"""