from django.template import Context
from openpyxl import Workbook

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

#
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_estate_email(location, recv_email):
    email_subject = '머니콜렉터 부동산/주식 정보'
    body = "<html>"
    body += "<h2>머니콜렉터 부동산/주식 정보 사이트 메일입니다.</h2>"
    body += f"<b>요청하신 {location} 지역에 관한 매물 정보입니다.</b>"
    body += "<b>궁금하거나 요청하실 사항이 있다면 아래 매일로 연락 부탁드립니다.</b><br><br>"
    body += "jihyung.kim.dev@gmail.com<br>"
    body += "</html>"

    email = EmailMultiAlternatives(
        email_subject, "msg.as_string()", settings.DEFAULT_FROM_EMAIL, [recv_email, ],)
    email.attach_alternative(body, "text/html")

    etcFileName = f'./report/estate/{location}.xlsx'
    with open(etcFileName, 'rb') as etcFD:
        etcPart = MIMEApplication(etcFD.read())
        etcPart.add_header('Content-Disposition',
                           'attachment', filename=location + "매물정보.xlsx")
        email.attach(etcPart)

    return email.send(fail_silently=False)


def send_stock_email(kind, page, recv_email):
    print("이거좀 보내라좀", kind, page)
    email_subject = '머니콜렉터 부동산/주식 정보'
    body = "<html>"
    body += "<h2>머니콜렉터 부동산/주식 정보 사이트 메일입니다.</h2>"
    body += f"<b>요청하신 {kind} {page} 순위에 관한 정보입니다.</b>"
    body += "<b>궁금하거나 요청하실 사항이 있다면 아래 매일로 연락 부탁드립니다.</b><br><br>"
    body += "jihyung.kim.dev@gmail.com<br>"
    body += "</html>"

    email = EmailMultiAlternatives(
        email_subject, "msg.as_string()", settings.DEFAULT_FROM_EMAIL, [recv_email, ],)
    email.attach_alternative(body, "text/html")

    etcFileName = f'./report/stock_main/{kind}_{page}.xlsx'
    with open(etcFileName, 'rb') as etcFD:
        etcPart = MIMEApplication(etcFD.read())
        etcPart.add_header('Content-Disposition',
                           'attachment', filename=kind + f"{page}순위정보.xlsx")
        email.attach(etcPart)
    return email.send(fail_silently=False)


def send_stock_detail_email(name, recv_email):
    email_subject = '머니콜렉터 부동산/주식 정보'
    body = "<html>"
    body += "<h2>머니콜렉터 부동산/주식 정보 사이트 메일입니다.</h2>"
    body += f"<b>요청하신 {name} 주식에 관한 상세 정보입니다.</b>"
    body += "<b>궁금하거나 요청하실 사항이 있다면 아래 매일로 연락 부탁드립니다.</b><br><br>"
    body += "jihyung.kim.dev@gmail.com<br>"
    body += "</html>"

    email = EmailMultiAlternatives(
        email_subject, "msg.as_string()", settings.DEFAULT_FROM_EMAIL, [recv_email, ],)
    email.attach_alternative(body, "text/html")

    etcFileName = f'./report/stock_detail/{name}.xlsx'
    with open(etcFileName, 'rb') as etcFD:
        etcPart = MIMEApplication(etcFD.read())
        etcPart.add_header('Content-Disposition',
                           'attachment', filename=f"{name} 정보.xlsx")
        email.attach(etcPart)

    return email.send(fail_silently=False)
