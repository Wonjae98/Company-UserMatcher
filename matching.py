import json
import json
import numpy as np
import itertools
from random import random, randrange

fieldName = ["Backend", "Frontend"]

fields = []
skill_list = [] # 분야별 필요한 스킬리스트
framework_list = [] # 분야별 필요한 프레임워크 리스트
etc_list = [] # 분야별 필요한 기타 리스트

user_dict = {'가나다': ['AI', 'Android', 'MongoDB', 'Python'],
             'abc': ['MySQL', 'DB', 'Java', 'MongoDB', 'Python', "Vue.js", 'NoSQL'],
             '123': ['HTML', 'CSS', 'Bootstrap', "Vue.js"]}


#각 분야별로 필요한 역량들이 나열된 json 파일을 로드한다.
def load_json():
    with open('data/Backend_skill.json', 'r') as json_file:
        fields.append(json.load(json_file))

    with open('data/Frontend_skill.json', 'r') as json_file:
        fields.append(json.load(json_file))


# 유저들이 가진 역량 정보와 기업이 원하는 역량 combine_list를 받고 상위 3명의 유저를 리턴해줌.        
def find_sim_user(user_info, combine_list): 
    user_match_count = {}
    for i, j in user_info.items():
        set1 = set(j) #유저의 역량 정보
        set2 = set(combine_list) #기업이 원하는 역량
        common_list = list(set1 & set2) # 일치하는 역량 리스트
        user_match_count[i] = len(common_list)

    user_match_count = dict(sorted(user_match_count.items(), key=lambda x: x[1], reverse=True))
    # user_match_count 딕셔너리를 일치하는 역량의 개수 순서대로 정렬해줌

    for i, j in list(user_match_count.items()):
        if j == 0:
            del (user_match_count[i])
    # user 딕셔너리에서 count가 0인 user 들은 삭제해줌

    user_match_count = list(user_match_count.items())
    user_name_top3 = []

    user_top3 = {}
    # 겹치는 스킬,프레임워크,기타가 0인 유저들을 제외한 나머지 유저들 중 상위 3명을 리턴해줌
    for i, j in enumerate(user_match_count):
        user_name_top3.append(user_match_count[i][0])

        for i, j in enumerate(user_name_top3):
            user_top3[j] = user_info[j]
    return user_top3, user_match_count

# 유저정보를 입력받고 유저id를 key로 갖는 딕셔너리로 리턴해줌.
def convert_user2this(user_info):
    result = {}
    for user in user_info:
        result[user["user_id"]] = user["skill"]
    return result

# 사용자 id와 skill, match ratio 를 결과로 리턴해줌.
def convert_user2result(user_info, match_count, company_skill_length):
    result = {"recommended_user": []}
    for user, count in zip(user_info.items(), match_count):
        part = {
            "user_id": user[0], #유저의 id
            "skill": user[1], #유저의 역량
            "match_ratio": count[1] / company_skill_length #ratio 계산을 위해 회사가 요구한 역량 개수로 나누어줌
        }
        result["recommended_user"].append(part)

    return result

# match_ratio를 기반으로 추천유저들을 리턴해줌
def match(user_info, company_skill_list):
    user_info_conv = convert_user2this(user_info) 
    result, match_count = find_sim_user(user_info_conv, company_skill_list["skill"]) #find_sim_user 함수를 호출하여 적합한 유저를 찾아줌
    result = convert_user2result(result, match_count, len(company_skill_list))  
    return result
