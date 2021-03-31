from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from crawling.util.crawling_estate import *
from crawling.util.crawling_stock_trend import *
from crawling.util.crawling_stock_detail import *
from crawling.util.crawling_stock_draw import *
from .models import Estate
from django.core.cache import cache
import json

# 캐싱과 논캐싱의 시간차이 (1.016 vs 0.003)
# import timeit
# start = timeit.default_timer()
# stop = timeit.default_timer()
# print("실제 걸리는 시간 차이", stop - start)


# 부동산정보
def crawl_estate(request):
    data = request.body.decode('utf-8')
    location = json.loads(data)['location']

    # 캐싱되어있지 않는 경우
    if not cache.get(location):
        try:
            location_url = util_crawling_start(location)
            search_url, extra_condition = get_location_condition(location_url)
            search_resp_dict, z = search_by_location_condition(
                search_url, extra_condition)
            all_danji_resp = get_all_resp(search_resp_dict, extra_condition)

            # 캐시에 없지만 db에는 데이터가 있습니다.
            if Estate.objects.filter(location=location).count() != 0:
                estate = Estate.objects.get(location=location)
                estate.estate_data = all_danji_resp
                estate.save()

            # 캐시에 없고 처음 삽입되는 데이터입니다.
            else:
                estate = Estate(location=location, estate_data=all_danji_resp)
                estate.save()

            # 캐시 셋팅
            set_cache_data = cache.set(location, all_danji_resp, 30)
        except:
            return JsonResponse({"msg": "데이터가 존재하지 않습니다."})

    get_data = cache.get(location)
    return JsonResponse({"all_danji_resp": get_data})


# 주식 트렌드
def crawl_stock_trend(request):
    data = request.body.decode('utf-8')
    sosok = json.loads(data)['sosok']
    page = int(json.loads(data)['page'])
    print(sosok, page, "소속과 페이지 받음")
    stocks_trend = crawl(sosok, page)
    return JsonResponse({"stocks_trend": "stocks_trend"})


# 주식 상세정보
def crawl_stock_detail(request):
    data = request.body.decode('utf-8')
    stock_name = json.loads(data)['stock_name']
    stock_code = get_code(stock_name)
    string_page = get_data_from_url(
        f"https://finance.naver.com/item/sise.nhn?code={stock_code}")
    stock_detail = parse(string_page)
    stock_detail['stock_name'] = stock_name
    return JsonResponse({"stock_detail": [stock_detail]})


# 주식 그려주기
def crawl_stock_draw(request):
    data = request.body.decode('utf-8')
    stock_name = json.loads(data)['stock_name']
    crawl(stock_name)
    return HttpResponse("잘됨?")
