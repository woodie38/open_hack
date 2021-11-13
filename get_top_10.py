# 이미지와 유사한 상위 10개의 관광지역의 이름과 순위를 list of 딕셔너리로 리턴.
def get_top_10():
    from PIL import Image
    import numpy as np
    import pandas as pd

    # 사용자 이미지 np배열로 변환
    image = './2614098.jpg'
    userImg = Image.open(image)
    userImgRgb = userImg.convert('RGB')
    userImgRgb = userImgRgb.resize((64,64))
    userRgbData = np.array(userImgRgb)

    # rgb데이터 가져오기
    dbData = pd.read_pickle('./rgb_data.pickle')    
    # 장소명데이터 가져오기
    dbtitle = pd.read_csv('./rgb_data.csv')
    # 혼잡도 데이터
    dbesit = pd.read_csv('./ymd_esti_data.csv')

    # 유클리드 거리계산  --- 추후 업데이트
    def euclid_dist(A,B):
        return np.linalg.norm(A - B)
    eu_dict = {}
    for i in range(len(dbData['rgb'])):
        eu_dict[dbtitle['galtitle'][i]] = euclid_dist(userRgbData, dbData['rgb'][i]) # 사용자사진과 거리계산
    eu_dict_10 = sorted(eu_dict.items(), key=lambda dist:dist[1])[:10]    # 정렬 후 상위 10개 {장소명 : 거리}

    # 해당 지역의 한달 평균 혼잡도 상위 10 추출
    esti_dict = {}
    for i in range(len(eu_dict_10)):
        esti_mean = dbesit[dbesit['title'] == eu_dict_10[i][0]]['estidecorat'].mean()
        esti_dict[eu_dict_10[i][0]] = esti_mean
    recom_space = sorted(esti_dict.items(), key=lambda x: x[1])
    pd.DataFrame(recom_space)

    # [{장소명 : 순위}]
    space_rank = []
    for i in range(len(recom_space)):
        space_rank.append({"name":recom_space[i][0],"similarity_rank":int(pd.DataFrame(recom_space)[1].rank()[i])})
    return space_rank

print(get_top_10())