from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from crawling.util.crawling_estate import *
from crawling.util.crawling_stock_trend import *
from crawling.util.crawling_stock_detail import *
from crawling.util.crawling_stock_draw import *
from .models import Estate, StockTrend, StockDetail
from django.core.cache import cache
import json
import timeit
import datetime

# start = timeit.default_timer()
# stop = timeit.default_timer()
# print("실제 걸리는 시간 차이", stop - start)
# 캐싱을 통해 약 150배 이상 속도 개선


# 부동산정보 # 캐싱과 논캐싱의 시간차이 (0.357 vs 0.006) 약60배
def crawl_estate(request):
    data = request.body.decode('utf-8')
    location = json.loads(data)['location']
    time_diff = 0

    # 계속 캐싱이 되는 경우 데이터를 갱신하지 않으므로
    # 마지막 수정시간과 현재시간의 차이를 구해서 그값을 기준으로 새로 데이터를 가져옴
    if Estate.objects.filter(location=location).exists():
        estate = Estate.objects.get(location=location)
        now = datetime.datetime.now()
        updated = estate.modified_at

        now_ = datetime.datetime.strptime(
            now.strftime('%H:%M:%S'), '%H:%M:%S')
        updated_ = datetime.datetime.strptime(
            updated.strftime('%H:%M:%S'), '%H:%M:%S')
        time_diff = ((now_ - updated_).seconds)/3600

   # 캐싱되어있지 않는 경우
    if not cache.get("estate"+location) or time_diff > 1:
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
            set_cache_data = cache.set(
                "estate"+location, all_danji_resp, 60*60)
        except:
            return JsonResponse({"msg": "데이터가 존재하지 않습니다."})
    get_data = cache.get("estate"+location)
    return JsonResponse({"all_danji_resp": get_data})


# 주식 트렌드 #캐싱과 논캐싱의 시간차이 (1.40 vs 0.009) 155배
def crawl_stock_trend(request):
    data = request.body.decode('utf-8')
    sosok = json.loads(data)['sosok']
    page = int(json.loads(data)['page'])
    time_diff = 0

    if StockTrend.objects.filter(sosok=sosok).filter(page=page).exists():
        stock = StockTrend.objects.filter(
            sosok=sosok).get(page=page)
        now = datetime.datetime.now()
        updated = stock.modified_at

        now_ = datetime.datetime.strptime(
            now.strftime('%H:%M:%S'), '%H:%M:%S')
        updated_ = datetime.datetime.strptime(
            updated.strftime('%H:%M:%S'), '%H:%M:%S')
        time_diff = ((now_ - updated_).seconds)/3600

    if not cache.get("trend" + sosok + str(page)) or time_diff > 1:
        try:
            stocks_trend = crawl_stock(sosok, page)
            # 캐시에 없지만 db에는 데이터가 있습니다.
            if StockTrend.objects.filter(sosok=sosok).filter(page=page).count() != 0:
                stock = StockTrend.objects.filter(
                    sosok=sosok).get(page=page)
                stock.sosok = sosok
                stock.page = page
                stock.trend_data = stocks_trend
                stock.save()
            # 캐시에 없고 처음 삽입되는 데이터입니다.
            else:
                stock = StockTrend(sosok=sosok, page=page,
                                   trend_data=stocks_trend)
                stock.save()
            # 캐시 셋팅
            set_cache_data = cache.set(
                "trend" + sosok + str(page), stocks_trend, 60*60)
        except:
            return JsonResponse({"msg": "데이터가 존재하지 않습니다."})
    trend_data = cache.get("trend" + sosok + str(page))
    return JsonResponse({"stocks_trend": trend_data})


# 주식 상세정보 #캐싱과 논캐싱의 시간차이 (2.32 vs 0.008) 290배
def crawl_stock_detail(request):
    data = request.body.decode('utf-8')
    stock_name = json.loads(data)['stock_name']
    time_diff = 0

    if StockDetail.objects.filter(stock_name=stock_name).exists() or time_diff > 1:
        stock = StockDetail.objects.get(stock_name=stock_name)
        now = datetime.datetime.now()
        updated = stock.modified_at

        now_ = datetime.datetime.strptime(
            now.strftime('%H:%M:%S'), '%H:%M:%S')
        updated_ = datetime.datetime.strptime(
            updated.strftime('%H:%M:%S'), '%H:%M:%S')
        time_diff = ((now_ - updated_).seconds)/3600

    # 캐시에 없음
    if not cache.get("detail" + stock_name):
        try:
            stock_code = get_code(stock_name)
            string_page = get_data_from_url(
                f"https://finance.naver.com/item/sise.nhn?code={stock_code}")
            stock_detail = parse(string_page)
            # stock_detail['stock_name'] = stock_name
            if StockDetail.objects.filter(stock_name=stock_name).count() != 0:
                stock = StockDetail.objects.get(stock_name=stock_name)
                stock.detail_data = stock_detail
                stock.save()

            # 캐시에 없고 처음 삽입되는 데이터입니다.
            else:
                stock = StockDetail(stock_name=stock_name,
                                    detail_data=stock_detail)
                stock.save()
            set_cache_data = cache.set(
                "detail"+stock_name, stock_detail, 60*60)
        except:
            return JsonResponse({"msg": "데이터가 존재하지 않습니다."})
    get_data = cache.get("detail"+stock_name)
    return JsonResponse({"stock_detail": [get_data]})


# 주식 그려주기 반응형 그래프
def crawl_stock_draw(request):
    data = request.body.decode('utf-8')
    stock_name = json.loads(data)['stock_name']
    crawl_draw(stock_name)
    return JsonResponse({"msg": stock_name})
