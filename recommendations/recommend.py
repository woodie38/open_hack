from PIL import Image
import numpy as np
import pandas as pd

def get_top_10_similarity(image, places):
    """
    Parameter image: 유저가 올린 이미지파일
    Precondition: 이미지 파일 유형이어야됨 

    Paramete places: places는 장고의 queryset object이다. 리스트랑 비슷하며 iterate할 수 있음. queryset 있는 object 하나마다 지역(place) object한개이다. 
    1. place object마다 rgb라는 필드를 보유함. Rgb는 numpy array. 
    2. place object마다 name(지역이름)라는 필드를 보유함. name필드는 string임


    ex) places.rgb = [[[31,23,45] , [150,203.230]..., [111,222,333]]]

    Precondition: 비어있지 않은 장고 queryset object
    
    get_top_10함수는 이미지와 가장 유사한 상위 10개의 관광지역의 이름과 순위를 list of dictionaries로 표현해서 return 한다
    ex) [{'name':'한옥마을' , 'similarity_rank' : 5 } , {'name':'홍대' , 'similarity_rank' : 2 } ... {'name':'해운대' , 'similarity_rank' : 1 }]
    """
    # 사용자 이미지 np배열로 변환
    #image = 'C:\\Users\\YI MORAN\\Downloads\\opendata_P\\photo_data\\user_photo\\2614098.jpg'
    userImg = Image.open(image)
    userImgRgb = userImg.convert('RGB')
    userImgRgb = userImgRgb.resize((64,64))
    userRgbData = np.array(userImgRgb)

    # 유클리드 거리계산  --- 추후 업데이트
    def euclid_dist(A,B):
        return np.linalg.norm(A - B)

    similarity_dict = {}
    for place in places: 
        place_name = place.name
        place_rgb = place.rgb 
        similarity_dict[place_name] = euclid_dist(userRgbData , place_rgb)
    similarity_dict = dict(sorted(similarity_dict.items(), key=lambda dist:dist[1])[:10])
    return similarity_dict

def get_top_10_copy(image, places):
    """
    Parameter image: 유저가 올린 이미지파일
    Precondition: 이미지 파일 유형이어야됨 

    Paramete places: places는 장고의 queryset object이다. 리스트랑 비슷하며 iterate할 수 있음. queryset 있는 object 하나마다 지역(place) object한개이다. 
    1. place object마다 rgb라는 필드를 보유함. Rgb는 numpy array. 
    2. place object마다 name(지역이름)라는 필드를 보유함. name필드는 string임


    ex) places.rgb = [[[31,23,45] , [150,203.230]..., [111,222,333]]]

    Precondition: 비어있지 않은 장고 queryset object
    
    get_top_10함수는 이미지와 가장 유사한 상위 10개의 관광지역의 이름과 순위를 list of dictionaries로 표현해서 return 한다
    ex) [{'name':'한옥마을' , 'similarity_rank' : 5 } , {'name':'홍대' , 'similarity_rank' : 2 } ... {'name':'해운대' , 'similarity_rank' : 1 }]
    """
    # 사용자 이미지 np배열로 변환
    #image = 'C:\\Users\\YI MORAN\\Downloads\\opendata_P\\photo_data\\user_photo\\2614098.jpg'
    userImg = image
    userImgRgb = userImg.convert('RGB')
    userImgRgb = userImgRgb.resize((64,64))
    userRgbData = np.array(userImgRgb)

    # rgb데이터 가져오기
    dbData = pd.read_pickle('../rgb_data.pickle')    
    # 장소명데이터 가져오기
    dbtitle = pd.read_csv('./rgb_data.csv')
    # 혼잡도 데이터
    dbesit = pd.read_csv('./ymd_esti_data.csv')

    # 유클리드 거리계산  --- 추후 업데이트
    def euclid_dist(A,B):
        return np.linalg.norm(A - B)

    eu_dict = {}


    for i in range(len(places)):
        eu_dict[dbtitle['galtitle'][i]] = euclid_dist(userRgbData, dbData['rgb'][i]) # 사용자사진과 거리계산
    eu_dict_10 = sorted(eu_dict.items(), key=lambda dist:dist[1])[:10]    # 정렬 후 상위 10개 {장소명 : 거리}

    # 해당 지역의 한달 평균 혼잡도 상위 10 추출
    esti_dict = {}
    for i in range(len(eu_dict_10)):
        esti_mean = dbesit[dbesit['title'] == eu_dict_10[i][0]]['estidecorat'].mean() # get the title that matches with the to 10 name. Get the estidecorat and find mean
        esti_dict[eu_dict_10[i][0]] = esti_mean # set the esti_dict name
    recom_space = sorted(esti_dict.items(), key=lambda x: x[1])
    pd.DataFrame(recom_space)

    # [{장소명 : 순위}]
    space_rank = []
    for i in range(len(recom_space)):
        space_rank.append({"name":recom_space[i][0],"similarity_rank":int(pd.DataFrame(recom_space)[1].rank()[i])})
    return space_rank

def get_bottom_3_covid(places):
    """
    Paramete places: places는 장고의 queryset object이다. 리스트랑 비슷하며 iterate할 수 있음. queryset 있는 object 하나마다 지역(place) object한개이다. 
    place object는 name (관과지 이름) 이라라는 필드를 보유함 
    ex) places.rgb = [[[31,23,45] , [150,203.230]..., [111,222,333]]]

    get_bottom_3 함수는 관광지역의 이름과 혼잡도 순의 하위 3개를 list of dictionaries로 표현해서 return 한다 
    [{'name':'한옥마을' , 'covid_rank' : 3 } , {'name':'홍대' , 'covid_rank' : 2  }, {'name':'해운대' , 'covid_rank' : 1 }]
    """



def get_rgb(image):
    """
    Parameter Image: image of one of the tourist attractions 
    Precondition: must be an image file

    returns the rgb values for the particular image"""
    pass

def euclid_dist(A,B):
    """
    Parameter A: matrix A that represents the RGB value of a matrix 
    Precondition: must be a numpy matrix that is 60*60 pixels

    Parameter B: matrix B that represents the RGB value of a matrix 
    Precondition: must be a numpy matrix that is 60*60 pixels

    Returns the euclidean_distance between the two matrices
    """
    return np.linalg.norm(A - B)

def get_top_10(list_of_dict): 
    """
    Parameter list_of_dict: list that contains dictionaries that possesses the name of the place as key and similarity score as its value
    Precondition: must be a dictionary that isn't empty
    
    Returns the list of names of the top 10 
    """
    pass

def partition(list_of_dicts, h, k):
    """
    Helper function for qsort
    """
    x_num = list_of_dicts[0]['similarity_rate'] 
    #h = 0
    #k = len(list_of_dicts)-1
    t = h+1
    j = k

    while(t<=j):
        t_num = list_of_dicts[t]['similarity_rate']
        j_num = list_of_dicts[j]['similarity_rate']
        if t_num < x_num:
            t += 1 
        elif j_num >= x_num: 
            j -= 1 
        else: # less than t greater than j 
            dict_temp = list_of_dicts[j]
            list_of_dicts[j] = dict_temp
            list_of_dicts[t] = dict_temp
            j -= 1 
            t += 1
    
    return j

def qsort(list_of_dicts , h , k):
    if k+1 - h <=1: 
        return 
    
    j = partition(list_of_dicts,h,k)
    temp_dict = list_of_dicts[0]
    list_of_dicts[0] = list_of_dicts[j]
    list_of_dicts[j] = temp_dict

    qsort(list_of_dicts,h, j-1)
    qsort(list_of_dicts,j+1, k)