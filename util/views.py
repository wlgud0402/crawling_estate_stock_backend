from django.shortcuts import render, HttpResponse

# Create your views here.


def crawling_estate():
    print("유틸앱 내부에 만든 크롤링 함수")
    return HttpResponse("gd")
