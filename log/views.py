from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def log_check(request):
    data = request.body.decode('utf-8')
    getData = json.loads(data)['data']
    print("요청받음", getData)
    return HttpResponse("로그체크: data")
