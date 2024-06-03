from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import Exchange
from rest_framework.decorators import api_view, permission_classes
from .serializers import ExchangeSerializer
import requests
from rest_framework.response import Response
from urllib.parse import unquote

EXC_API_KEY = settings.EXC_API_KEY
BASE_URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
@api_view(['GET'])
def get_exchange_rate(request):
    params = {
        'authkey': EXC_API_KEY,
        'searchdate': '20240517', # 비영업일 데이터는 제공하지 않으므로 임시로 날짜 지정
        'data': 'AP01',
    }
    print('hi')
    response = requests.get(BASE_URL, params=params).json()
    return Response({'response' : response})


@api_view(['GET'])
def save_exchange_data(request):
    params = {
        'authkey': EXC_API_KEY,
        'searchdate': '20240517', # 비영업일 데이터는 제공하지 않으므로 임시로 날짜 지정
        'data': 'AP01',
    }
    
    countries = requests.get(BASE_URL, params=params).json()
    for country in countries:
        cur_unit = country.get('cur_unit')
        ttb = float(country.get('ttb').replace(',',''))
        tts = float(country.get('tts').replace(',',''))
        kftc_deal_bas_r = float(country.get('kftc_deal_bas_r').replace(',',''))
        print(cur_unit)
        save_country_data = {
            'cur_unit' : cur_unit,
            'ttb' : ttb,
            'tts' : tts,
            'kftc_deal_bas_r' : kftc_deal_bas_r,
        }
        
        exchange_serializer = ExchangeSerializer(data=save_country_data)
        if exchange_serializer.is_valid(raise_exception=True):
            exchange_serializer.save()
    return JsonResponse({'message':'저장완료'})
    
@api_view(['GET'])
def k_to_f(request, won, country):
    # won를 float 타입으로 변환
    won = float(won)
    print(won)
    # target_country에 해당하는 Exchange 객체 가져오기
    exchange_rate = Exchange.objects.get(cur_unit=country).kftc_deal_bas_r

    
    # 계산
    result = won / exchange_rate

    # 소수점 둘 째 자리까지만
    result = round(result, 2)
    
    # 결과 반환
    return JsonResponse({'result': result})

@api_view(['GET'])
def f_to_k(request, foreign_money, country):
    # won를 float 타입으로 변환
    foreign_money = float(foreign_money)
    
    # target_country에 해당하는 Exchange 객체 가져오기
    exchange_rate = Exchange.objects.get(cur_unit=country).kftc_deal_bas_r

    
    # 계산
    result = foreign_money * exchange_rate
    
    # 소수점 둘 째 자리까지만
    result = round(result, 2)
    
    # 결과 반환
    return JsonResponse({'result': result})

@api_view(['GET'])
def check_exchange_data(request):
    from .models import Exchange
    data_exists = Exchange.objects.exists()
    return JsonResponse({'data_exists': data_exists})