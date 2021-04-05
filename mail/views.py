from django.http import JsonResponse
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from openpyxl import Workbook
import jwt
from user.models import User


def send_mail_estate(request):
    # 받은 데이터
    try:
        data = request.body.decode('utf-8')
        encoded_jwt = json.loads(data)['token']
        location = json.loads(data)['location']
        estate_json_data = json.loads(data)['data']
        user_token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user = User.objects.get(id=user_token.get('id'))
        secret_file = './config/mail.json'
        with open(secret_file, "r") as f:
            secrets = json.loads(f.read())

        # 이메일 관련
        sendEmail = secrets['SEND_EMAIL']
        recvEmail = user.email  # 받는사람의 이메일 정보
        password = secrets['MAIL_PASSWORD']
        smtpName = "smtp.gmail.com"  # smtp 서버 주소
        smtpPort = 587  # smtp 포트 번호

        msg = MIMEMultipart()
        msg['Subject'] = f"머니콜렉터 : {location} 매물정보"
        msg['From'] = "머니콜렉터 부동산/주식 정보"
        msg['To'] = recvEmail

        body = "<html>"
        body += "<h2>머니콜렉터 부동산/주식 정보 사이트 메일입니다.</h2>"
        body += f"<b>요청하신 {location} 지역에 관한 매물 정보입니다.</b>"
        body += "<b>궁금하거나 요청하실 사항이 있다면 아래 매일로 연락 부탁드립니다.</b><br><br>"
        body += "jihyung.kim.dev@gmail.com<br>"
        body += "</html>"
        bodypart = MIMEText(body, "html")
        msg.attach(bodypart)

        wb = Workbook()  # create xlsx file
        ws = wb.active  # create xlsx sheet

        # 첫번째 줄 헤더
        ws.append([
            "아파트명",
            "건물타입",
            "빌딩타입",
            "동수",
            "세대수",
            "사용승인일",
            "대표이미지",
            "가용매매",
            "가용전세",
            "가용월세",
            "가용단기",
            "총가용",
            "최소면적",
            "최대면적",
            "최소매매가",
            "최대매매가",
            "최소전세가",
            "최대전세가",
        ])
        for i in range(len(estate_json_data)):
            ws.append([estate_json_data[i].get("hscpNm"),
                       estate_json_data[i].get("hscpTypeCd"),
                       estate_json_data[i].get("hscpTypeNm"),
                       estate_json_data[i].get("totDongCnt"),
                       estate_json_data[i].get("totHsehCnt"),
                       estate_json_data[i].get("useAprvYmd"),
                       estate_json_data[i].get("repImgUrl"),
                       estate_json_data[i].get("dealCnt"),
                       estate_json_data[i].get("leaseCnt"),
                       estate_json_data[i].get("rentCnt"),
                       estate_json_data[i].get("strmRentCnt"),
                       estate_json_data[i].get("totalAtclCnt"),
                       estate_json_data[i].get("minSpc"),
                       estate_json_data[i].get("maxSpc"),
                       estate_json_data[i].get("dealPrcMin"),
                       estate_json_data[i].get("dealPrcMax"),
                       estate_json_data[i].get("leasePrcMin"),
                       estate_json_data[i].get("leasePrcMax")])
        wb.save(f'./report/estate/{location}.xlsx')

        # 파일 추가
        etcFileName = f'./report/estate/{location}.xlsx'
        with open(etcFileName, 'rb') as etcFD:
            etcPart = MIMEApplication(etcFD.read())
            # 첨부파일의 정보를 헤더로 추가
            etcPart.add_header('Content-Disposition',
                               'attachment', filename=location + "매물정보.xlsx")
            msg.attach(etcPart)

        s = smtplib.SMTP(smtpName, smtpPort)
        s.starttls()
        s.login(sendEmail, password)
        s.sendmail(sendEmail, recvEmail, msg.as_string())
        s.close()
        return JsonResponse({"msg": "이메일이 발송되었습니다."})
    except:
        return JsonResponse({"msg": "오류가 발생했습니다. 로그인을 다시 진행해 주세요."})


def send_mail_stock(request):
    try:
        data = request.body.decode('utf-8')
        encoded_jwt = json.loads(data)['token']
        user_token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user = User.objects.get(id=user_token.get('id'))

        stock_json_data = json.loads(data)['data']
        kind = json.loads(data)['kind']
        page = (int(json.loads(data)['page'])-1) * 50

        if kind == "0":
            kind = "코스피"
        else:
            kind = "코스닥"

        secret_file = './config/mail.json'
        with open(secret_file, "r") as f:
            secrets = json.loads(f.read())

        sendEmail = secrets['SEND_EMAIL']
        recvEmail = user.email
        password = secrets['MAIL_PASSWORD']
        smtpName = "smtp.gmail.com"
        smtpPort = 587

        msg = MIMEMultipart()
        msg['Subject'] = f"머니콜렉터 : {kind} 랭킹 정보"
        msg['From'] = "머니콜렉터 부동산/주식 정보"
        msg['To'] = recvEmail

        body = "<html>"
        body += "<h2>머니콜렉터 부동산/주식 정보 사이트 메일입니다.</h2>"
        body += f"<b>요청하신 {kind} {page} 순위에 관한 정보입니다.</b>"
        body += "<b>궁금하거나 요청하실 사항이 있다면 아래 매일로 연락 부탁드립니다.</b><br><br>"
        body += "jihyung.kim.dev@gmail.com<br>"
        body += "</html>"
        bodypart = MIMEText(body, "html")
        msg.attach(bodypart)

        wb = Workbook()
        ws = wb.active

        ws.append([
            "순위",
            "이름",
            "코드",
            "현재가",
            "시가총액",
            "거래량",
            "전일대비",
            "등락율",
        ])
        for i in range(len(stock_json_data)):
            ws.append([stock_json_data[i].get("rank"),
                       stock_json_data[i].get("name"),
                       stock_json_data[i].get("code"),
                       stock_json_data[i].get("now_price"),
                       stock_json_data[i].get("total_price"),
                       stock_json_data[i].get("trade_amount"),
                       stock_json_data[i].get("compare_yesterday_money"),
                       stock_json_data[i].get("compare_yesterday_proportion")])

        wb.save(f'./report/stock_main/{kind}_{page}.xlsx')
        etcFileName = f'./report/stock_main/{kind}_{page}.xlsx'
        with open(etcFileName, 'rb') as etcFD:
            etcPart = MIMEApplication(etcFD.read())
            # 첨부파일의 정보를 헤더로 추가
            etcPart.add_header('Content-Disposition',
                               'attachment', filename=kind + f"{page}순위정보.xlsx")
            msg.attach(etcPart)

        s = smtplib.SMTP(smtpName, smtpPort)
        s.starttls()
        s.login(sendEmail, password)
        s.sendmail(sendEmail, recvEmail, msg.as_string())
        s.close()

        return JsonResponse({"msg": "이메일이 발송되었습니다."})
    except:
        return JsonResponse({"msg": "오류가 발생했습니다. 로그인을 다시 진행해 주세요."})


def send_mail_stock_detail(request):
    try:
        data = request.body.decode('utf-8')
        encoded_jwt = json.loads(data)['token']
        user_token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user = User.objects.get(id=user_token.get('id'))

        detail_json_data = json.loads(data)['data']
        name = json.loads(data)['name']

        secret_file = './config/mail.json'
        with open(secret_file, "r") as f:
            secrets = json.loads(f.read())

        sendEmail = secrets['SEND_EMAIL']
        recvEmail = user.email
        password = secrets['MAIL_PASSWORD']
        smtpName = "smtp.gmail.com"
        smtpPort = 587

        msg = MIMEMultipart()
        msg['Subject'] = f"머니콜렉터 : {name}주식 상세 정보"
        msg['From'] = "머니콜렉터 부동산/주식 정보"
        msg['To'] = recvEmail

        body = "<html>"
        body += "<h2>머니콜렉터 부동산/주식 정보 사이트 메일입니다.</h2>"
        body += f"<b>요청하신 {name} 주식에 관한 상세 정보입니다.</b>"
        body += "<b>궁금하거나 요청하실 사항이 있다면 아래 매일로 연락 부탁드립니다.</b><br><br>"
        body += "jihyung.kim.dev@gmail.com<br>"
        body += "</html>"
        bodypart = MIMEText(body, "html")
        msg.attach(bodypart)

        wb = Workbook()
        ws = wb.active

        ws.append([
            "현재가",
            "매도호가",
            "매수호가",
            "등락율",
            "전일대비",
            "전일가",
            "거래량",
            "시가",
            "고가",
            "저가",
            "거래대금(천)",
            "액면가",
            "상한가",
            "하한가",
            "전일상한",
            "전일하한",
            "PER",
            "EPS",
            "high_52",
            "low_52",
            "시가총액",
            "상장주식수",
            "외국인현재",
            "자본금",
        ])
        for i in range(len(detail_json_data)):
            ws.append([detail_json_data[i].get("now_price"),
                       detail_json_data[i].get("sell_price"),
                       detail_json_data[i].get("buy_price"),
                       detail_json_data[i].get("compare_yesterday_proportion"),
                       detail_json_data[i].get("compare_yesterday_money"),
                       detail_json_data[i].get("yesterday_price"),
                       detail_json_data[i].get("trade_amount"),
                       detail_json_data[i].get("start_price"),
                       detail_json_data[i].get("high_price"),
                       detail_json_data[i].get("low_price"),
                       detail_json_data[i].get("income_momey"),
                       detail_json_data[i].get("face_price"),
                       detail_json_data[i].get("high_limit"),
                       detail_json_data[i].get("yesterday_high_limit"),
                       detail_json_data[i].get("low_limit"),
                       detail_json_data[i].get("yesterday_low_limit"),
                       detail_json_data[i].get("PER"),
                       detail_json_data[i].get("EPS"),
                       detail_json_data[i].get("high_52"),
                       detail_json_data[i].get("low_52"),
                       detail_json_data[i].get("total_price"),
                       detail_json_data[i].get("market_sale_count"),
                       detail_json_data[i].get("foreigner"),
                       detail_json_data[i].get("have_momey")])

        wb.save(f'./report/stock_detail/{name}.xlsx')
        etcFileName = f'./report/stock_detail/{name}.xlsx'
        with open(etcFileName, 'rb') as etcFD:
            etcPart = MIMEApplication(etcFD.read())
            etcPart.add_header('Content-Disposition',
                               'attachment', filename=f"{name} 정보.xlsx")
            msg.attach(etcPart)

        s = smtplib.SMTP(smtpName, smtpPort)
        s.starttls()
        s.login(sendEmail, password)
        s.sendmail(sendEmail, recvEmail, msg.as_string())
        s.close()

        return JsonResponse({"msg": "이메일이 발송되었습니다."})
    except:
        return JsonResponse({"msg": "오류가 발생했습니다. 로그인을 다시 진행해 주세요."})
