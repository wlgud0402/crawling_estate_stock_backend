from django.shortcuts import render, HttpResponse


def log_check(request):
    return HttpResponse("로그체크")
