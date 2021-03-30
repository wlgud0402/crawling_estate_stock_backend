from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from crawling.util.crawling_estate import *
from crawling.util.crawling_stock_trend import *
from crawling.util.crawling_stock_detail import *
from crawling.util.crawling_stock_draw import *
import json


# 부동산정보
def crawl_estate(request):
    data = request.body.decode('utf-8')
    location = json.loads(data)['location']
    location_url = util_crawling_start(location)
    search_url, extra_condition = get_location_condition(location_url)
    search_resp_dict, z = search_by_location_condition(
        search_url, extra_condition)
    all_danji_resp = get_all_resp(search_resp_dict, extra_condition)
    return JsonResponse({"all_danji_resp": all_danji_resp})


# 주식 트렌드
def crawl_stock_trend(request):
    data = request.body.decode('utf-8')
    sosok = json.loads(data)['sosok']
    page = int(json.loads(data)['page'])
    stocks_trend = crawl(sosok, page)
    return JsonResponse({"stocks_trend": stocks_trend})


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
