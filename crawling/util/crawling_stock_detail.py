# # "https://finance.naver.com/item/sise.nhn?code=051910"
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px


def get_code(stock_name):
    company = stock_name.upper()
    header = {
        'User-Agent': 'Mozilla/5.0 (MacintoshIntel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    }

    stock_code = pd.read_html(
        'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    stock_code.sort_values(['상장일'], ascending=True)
    stock_code = stock_code[['회사명', '종목코드']]
    stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})
    stock_code.code = stock_code.code.map('{:06d}'.format)
    code = stock_code[stock_code.company ==
                      company].code.values[0].strip()
    return code


def parse(page_string):
    bsObj = BeautifulSoup(page_string, "html.parser")
    content_box = bsObj.findAll('tbody')[0]
    content_all_tr = content_box.findAll('tr')
    #
    now_price = content_all_tr[0].findAll('td')[0].text.strip()
    sell_price = content_all_tr[0].findAll('td')[1].text.strip()
    compare_yesterday_money = content_all_tr[1].findAll('td')[0].text.strip()
    buy_price = content_all_tr[1].findAll('td')[1].text.strip()
    compare_yesterday_proportion = content_all_tr[2].findAll('td')[
        0].text.strip()
    yesterday_price = content_all_tr[2].findAll('td')[1].text.strip()
    trade_amount = content_all_tr[3].findAll('td')[0].text.strip()
    start_price = content_all_tr[3].findAll('td')[1].text.strip()
    income_momey = content_all_tr[4].findAll('td')[0].text.strip()
    high_price = content_all_tr[4].findAll('td')[1].text.strip()
    face_price = content_all_tr[5].findAll('td')[0].text.strip()
    low_price = content_all_tr[5].findAll('td')[1].text.strip()
    high_limit = content_all_tr[7].findAll('td')[0].text.strip()
    yesterday_high_limit = content_all_tr[7].findAll('td')[1].text.strip()
    low_limit = content_all_tr[8].findAll('td')[0].text.strip()
    yesterday_low_limit = content_all_tr[8].findAll('td')[1].text.strip()
    PER = content_all_tr[9].findAll('td')[0].text.strip()
    EPS = content_all_tr[9].findAll('td')[1].text.strip()
    high_52 = content_all_tr[10].findAll('td')[0].text.strip()
    low_52 = content_all_tr[10].findAll('td')[1].text.strip()
    total_price = content_all_tr[11].findAll('td')[0].text.strip()
    market_sale_count = content_all_tr[11].findAll('td')[1].text.strip()
    foreigner = content_all_tr[12].findAll('td')[0].text.strip()
    have_momey = content_all_tr[12].findAll('td')[1].text.strip()
    #
    return{"now_price": now_price, "sell_price": sell_price, "buy_price": buy_price,
           "compare_yesterday_proportion": compare_yesterday_proportion, "compare_yesterday_money": compare_yesterday_money,
           "yesterday_price": yesterday_price, "trade_amount": trade_amount, "start_price": start_price,
           "high_price": high_price, "low_price": low_price, "income_momey": income_momey,
           "face_price": face_price, "high_limit": high_limit, "yesterday_high_limit": yesterday_high_limit,
           "low_limit": low_limit, "yesterday_low_limit": yesterday_low_limit,
           "PER": PER, "EPS": EPS, "high_52": high_52, "low_52": low_52, "total_price": total_price,
           "market_sale_count": market_sale_count, "foreigner": foreigner, "have_momey": have_momey}


def get_data_from_url(url):
    data = requests.get(url)
    return data.content


def crawl_detail():
    code = "051910"
    string_page = get_data_from_url(
        f"https://finance.naver.com/item/sise.nhn?code={code}")
    stock_detail = parse(string_page)
    return stock_detail
