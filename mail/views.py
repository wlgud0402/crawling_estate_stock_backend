from django.http import JsonResponse
from django.http import HttpResponse
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from openpyxl import Workbook
import jwt
from user.models import User
from mail.tasks import send_estate_task, send_stock_detail_task, send_stock_task
from .utils import json_estate_to_xlsx, json_stock_detail_to_xlsx, json_stock_to_xlsx


def send_mail_estate_by_celery(request):
    try:
        data = request.body.decode('utf-8')
        encoded_jwt = request.META.get('HTTP_TOKEN')
        location = json.loads(data)['location']
        estate_json_data = json.loads(data)['data']
        user_token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user = User.objects.get(id=user_token.get('id'))
        user_mail = user.email

        json_estate_to_xlsx(location, estate_json_data)

        send_estate_task.delay(location, user_mail)
        msg = "이메일이 발송되었습니다."
        return JsonResponse({"msg": msg})
    except:
        msg = "오류가 발생했습니다. 로그인을 다시 진행해 주세요."
        return JsonResponse({"msg": msg})


def send_mail_stock_by_celery(request):
    try:
        data = request.body.decode('utf-8')
        encoded_jwt = request.META.get('HTTP_TOKEN')
        user_token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user = User.objects.get(id=user_token.get('id'))
        user_mail = user.email

        stock_json_data = json.loads(data)['data']
        kind = json.loads(data)['kind']

        if kind == "0":
            kind = "코스피"
        else:
            kind = "코스닥"

        page = (int(json.loads(data)['page'])-1) * 50

        json_stock_to_xlsx(kind, page, stock_json_data)
        print("json성공", kind, page, user_mail)
        send_stock_task.delay(kind, page, user_mail)
        msg = "이메일이 발송되었습니다."
        return JsonResponse({"msg": msg})
    except:
        msg = "오류가 발생했습니다. 로그인을 다시 진행해 주세요."
        return JsonResponse({"msg": msg})


def send_mail_stock_detail_by_celery(request):
    try:
        data = request.body.decode('utf-8')
        encoded_jwt = request.META.get('HTTP_TOKEN')
        user_token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user = User.objects.get(id=user_token.get('id'))
        user_mail = user.email
        detail_json_data = json.loads(data)['data']
        name = json.loads(data)['name']

        json_stock_detail_to_xlsx(name, detail_json_data)

        send_stock_detail_task.delay(name, user_mail)
        msg = "이메일이 발송되었습니다."
        return JsonResponse({"msg": msg})
    except:
        msg = "오류가 발생했습니다. 로그인을 다시 진행해 주세요."
        return JsonResponse({"msg": msg})
