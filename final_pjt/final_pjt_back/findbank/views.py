from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

MAP_API_KEY = settings.MAP_API_KEY
# Create your views here.
def find(request):
    return JsonResponse({'API_KEY': MAP_API_KEY})