import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px


def crawl_draw(inputStockName):
    company = inputStockName.upper()
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

    df = pd.DataFrame()
    for page in range(1, 21):
        base_url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
        detail_url = f'{base_url}&page={page}'
        stock_info = requests.get(detail_url, headers=header)
        df = df.append(pd.read_html(stock_info.text, header=0)
                       [0], ignore_index=True)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()

    # 한글로 된 컬럼명을 영어로 바꿔줌
    df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                            '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
    # 데이터의 타입을 int형으로 바꿔줌
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[[
        'close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df['date'] = pd.to_datetime(df['date'])

    # 일자(date)를 기준으로 오름차순 정렬
    df = df.sort_values(by=['date'], ascending=True)

    fig = px.line(df, x='date', y='close',
                  title='{}의 종가'.format(company))

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()
