from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

CHT_API_KEY = settings.CHT_API_KEY
# Create your views here.
def find(request):
    return JsonResponse({'API_KEY': CHT_API_KEY})