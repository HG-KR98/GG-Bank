from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.get_exchange_rate),
    path('save/', views.save_exchange_data),
    path('k_to_f/<str:won>/<str:country>/', views.k_to_f),
    path('f_to_k/<str:foreign_money>/<str:country>/', views.f_to_k),
    path('check/', views.check_exchange_data),
]
