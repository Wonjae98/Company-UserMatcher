import json
import json
import numpy as np
import itertools
from random import random, randrange

fieldName = ["Backend", "Frontend"]

fields = []
skill_list = []
framework_list = []
etc_list = []

user_dict = {'가나다': ['AI', 'Android', 'MongoDB', 'Python'],
             'abc': ['MySQL', 'DB', 'Java', 'MongoDB', 'Python', "Vue.js", 'NoSQL'],
             '123': ['HTML', 'CSS', 'Bootstrap', "Vue.js"]}


def load_json():
    with open('data/Backend_skill.json', 'r') as json_file:
        fields.append(json.load(json_file))

    with open('data/Frontend_skill.json', 'r') as json_file:
        fields.append(json.load(json_file))


def find_sim_user(user_info, combine_list):
    user_match_count = {}
    for i, j in user_info.items():
        set1 = set(j)
        set2 = set(combine_list)
        common_list = list(set1 & set2)
        user_match_count[i] = len(common_list)

    user_match_count = dict(sorted(user_match_count.items(), key=lambda x: x[1], reverse=True))
    ## user_match_count 딕셔너리를 value 순서대로 정렬해줌

    for i, j in list(user_match_count.items()):
        if j == 0:
            del (user_match_count[i])
    ## user 딕셔너리에서 count가 0인 user 들은 삭제해줌

    user_match_count = list(user_match_count.items())
    user_name_top3 = []

    ## 겹치는 스킬,프레임워크,기타가 0인 유저들을 제외한 나머지 유저들 중 상위 3명을 리턴해줌
    for i, j in enumerate(user_match_count):
        user_name_top3.append(user_match_count[i][0])

        user_top3 = {}
        for i, j in enumerate(user_name_top3):
            user_top3[j] = user_info[j]
    return user_top3, user_match_count


def convert_user2this(user_info):
    result = {}
    for user in user_info:
        result[user["user_id"]] = user["skill"]
    return result


def convert_user2result(user_info, match_count, company_skill_length):
    result = {"recommended_user": []}
    for user, count in zip(user_info.items(), match_count):
        part = {
            "user_id": user[0],
            "skill": user[1],
            "match_ratio": count[1] / company_skill_length
        }
        result["recommended_user"].append(part)

    return result


def match(user_info, company_skill_list):
    user_info_conv = convert_user2this(user_info)
    result, match_count = find_sim_user(user_info_conv, company_skill_list["skill"])
    result = convert_user2result(result, match_count, len(company_skill_list))
    return result
