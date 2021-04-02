import requests
from bs4 import BeautifulSoup
import json
import re
# from openpyxl import Workbook


def get_data_from_url(url):
    data = requests.get(url)
    return data.content


def get_stock_info(tr):
    all_td = tr.findAll('td')
    rank = all_td[0].text
    href = all_td[1].find('a')
    link = "https://finance.naver.com" + href['href']
    name = href.text
    code = href['href'][-6:]
    now_price = all_td[2].text
    compare_yesterday_money_extra = all_td[3].text
    compare_yesterday_proportion_extra = all_td[4].text
    compare_yesterday_money = re.sub(
        '\n|\t', '', compare_yesterday_money_extra)
    compare_yesterday_proportion = re.sub(
        '\n|\t', '', compare_yesterday_proportion_extra)
    total_price = all_td[6].text
    trade_amount = all_td[9].text
    return {"rank": rank, "name": name,
            # "link": link,
            "code": code, "now_price": now_price,
            "total_price": total_price, "trade_amount": trade_amount,
            "compare_yesterday_money": compare_yesterday_money,
            "compare_yesterday_proportion": compare_yesterday_proportion}


def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    content_box = bsObj.find('div', {"class": "box_type_l"})
    content_table = content_box.find('table', {"class": "type_2"})
    content_table_tbody = content_table.find("tbody")
    content_table_tbody_tr = content_table_tbody.findAll('tr')
    all_stock_info = []
    for tr in content_table_tbody_tr:
        try:
            stock_info = get_stock_info(tr)
            all_stock_info.append(stock_info)
        except Exception as e:
            continue
    return all_stock_info


def get_sise_market_sum(sosok, page):
    url = f"https://finance.naver.com/sise/sise_market_sum.nhn?sosok={sosok}&page={page}"
    pageString = get_data_from_url(url)
    stock_list = parse(pageString)
    return stock_list


# sosok: 0 => 코스피, 1 => 코스닥
def crawl_stock(sosok, pages):
    result = []
    for page in range(1, pages):
        stock_list = get_sise_market_sum(sosok, page)
        result += stock_list
    return result
