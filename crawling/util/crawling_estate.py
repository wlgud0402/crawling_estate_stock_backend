from django.shortcuts import render, HttpResponse
import requests
import json
import math


def util_crawling_start(location):
    location_url = f"https://m.land.naver.com/search/result/{location}"
    return location_url


def get_location_condition(location_url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
        'Referer': 'https://m.land.naver.com/'
    }
    location_resp = requests.get(location_url, headers=header)
    # filter를 기준으로 split후에 여러 조건들을 찾는다
    start_idx = location_resp.text.find("filter")
    end_idx = start_idx + 224

    # 여러가지 조건들
    condition = location_resp.text[start_idx:end_idx]
    lat = condition.split(",")[0].split("\'")[1]
    lon = condition.split(",")[1].split("\'")[1]
    z = condition.split(",")[2].split("\'")[1]
    cortarNo = condition.split(",")[3].split("\'")[1]

    search_type = "APT"
    building_type = "A1:B1:B2"

    extra_condition = {
        "z": z,
        "cortarNo": cortarNo,
        "search_type": search_type,
        "building_type": building_type,
        "header": header,
    }

    # 조건을 갖춘 URL
    search_url = f"https://m.land.naver.com/cluster/clusterList?cortarNo={cortarNo}&rletTpCd={search_type}&tradTpCd={building_type}&z={z}&lat={lat}&lon={lon}&addon=COMPLEX&bAddon=COMPLEX&isOnlylsale=false"
    return search_url, extra_condition


def search_by_location_condition(search_url, extra_condition):
    header = extra_condition['header']
    # 상세 조건을 바탕으로 여러 단지에 대한 정보를 세분화 하여 저장
    search_resp = requests.get(search_url, headers=header)
    search_resp_json = json.loads(search_resp.text).get('data').get('COMPLEX')

    search_resp_dict = {}
    for i in range(len(search_resp_json)):
        search_resp_dict[i] = {}
        search_resp_dict[i]['lgeo'] = search_resp_json[i]['lgeo']
        search_resp_dict[i]['lat'] = search_resp_json[i]['lat']
        search_resp_dict[i]['lon'] = search_resp_json[i]['lon']
        search_resp_dict[i]['count'] = search_resp_json[i]['count']
    return search_resp_dict, extra_condition


def get_all_resp(search_resp_dict, extra_condition):
    search_type = extra_condition['search_type']
    building_type = extra_condition['building_type']
    z = extra_condition['z']
    cortarNo = extra_condition['cortarNo']
    header = extra_condition['header']

    all_danji_resp = []
    for i in range(len(search_resp_dict)):
        danji_lgeo = search_resp_dict[i]['lgeo']
        danji_lat = search_resp_dict[i]['lat']
        danji_lon = search_resp_dict[i]['lon']
        danji_count = search_resp_dict[i]['count']
        page_count = math.ceil(danji_count/20)
        for page in range(1, page_count+1):
            each_danji_url = f"https://m.land.naver.com/cluster/ajax/complexList?itemId={danji_lgeo}&mapKey=&lgeo={danji_lgeo}&rletTpCd={search_type}&tradTpCd={building_type}&z={z}&lat={danji_lat}&lon={danji_lon}&cortarNo={cortarNo}&isOnlylsale=false&sort=readRank&page={page}"
            each_danji_resp = requests.get(each_danji_url, headers=header)
            each_danji_json = json.loads(each_danji_resp.text).get('result')
            for j in range(len(each_danji_json)):
                one_info = {}
                for key, value in each_danji_json[j].items():
                    # 데이터에서 불필요한거 제거 ex)<div>
                    if key == "dealPrcMin" or key == "dealPrcMax" or \
                            key == "leasePrcMin" or key == "leasePrcMax":
                        value = value[:value.find(
                            "<")] + value[value.find(">")+1:]
                        value = value[:value.find(
                            "<")] + value[value.find(">")+1:]
                    if key == "repImgUrl":
                        imgurl = "https://landthumb-phinf.pstatic.net" + value
                        value = imgurl
                    one_info[key] = value
                del one_info['hscpNo']
                del one_info['genHsehCnt']
                del one_info['isalePrcMin']
                del one_info['isalePrcMax']
                del one_info['isaleNotifSeq']
                del one_info['isaleScheLabel']
                del one_info['isaleScheLabelPre']
                all_danji_resp.append(one_info)
    return all_danji_resp
