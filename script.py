import pandas as pd 
import numpy as np
import pickle 
from recommendations.models import Foot_Traffic, Places 
from glob import glob 

def get_final_dict():
    # first get the df
    rgb_df = pd.read_csv('rgb_data.csv')
    rgb_df.drop('rgb' , inplace = True, axis = 1)

    with open('rgb_data.pickle',"rb") as fr: 
        df = pickle.load(fr)
    s = df['rgb'] 
    count = 0
    for index, value in s.iteritems():
        if count==0: 
            # first row
            val = value[0]
            #print(val, type(value), len(val))
            count+=1
        else:
            break

    rgb_df['rgb'] = s
    df_records = rgb_df.to_dict('records') 
    return df_records

#rgb_df is a df with numpy type in column rgb

#df_records = rgb_df.to_dict('records') 

"""f_records = get_final_dict()
count = 0 
for record in df_records: 
    if count == 0: 
        name = record['galtitle']
        image_url= record['galwebimageurl']
        rgb = record['rgb']
        p = Places(name = name, image_url = image_url,rgb = rgb)
        p.save()
    else: 
        break"""
def place_images():
    places_list = Places.objects.order_by("id")
    
    count = 0
    for place in places_list: 
        
        count_str = str(count)
        img = 'photo370(num)/' + count_str +".jpg"
        place.image = img
        count += 1
        place.save()
    

def list_image_names(): 
    count =0 
    for file in glob('photo370(num)/*'):
        if count < 10: 
            print(file, type(file))
            count+=1


def get_rgb():
    count = 0 
    places = Places.objects.all()
    for place in places: 
        if count<5:
            print(place.rgb)
        else:
            break

def set_location():
    foot_traffic = pd.read_csv('foot_traffic.csv')
    foot_traffic.drop_duplicates(subset = "title" , inplace = True)
    location = foot_traffic['galphotographylocation']
    l = location.to_list()

    count = 0
    places = Places.objects.all()
    for place in places:
        place_location = l[count] 
        place.location = place_location
        place.save()
        count+=1

def set_foottraffic():
    foot_traffic_df = pd.read_csv('foot_traffic.csv')
    df_records = foot_traffic_df.to_dict('records')

    

    #model_instances = [Foot_Traffic(place = Foot_Traffic.objects.get(place__name=record['title']),
                                    #traffic_level  = record['estidecorat'] , 
                                    #date = record['baseymd'])
                                    # for record in df_records]
    count = 0 
    for record in df_records: 
        if count <3:
            place_name = record['title']
            traffic = record['estidecorat']
            date = record['baseymd']

            place =Places.objects.get(name = place_name)
            Foot_Traffic.objects.create(place=place, traffic_level = traffic, date = date)
        else:
            break

    #Foot_Traffic.objects.bulk_create(model_instances)


