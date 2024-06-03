from django.urls import path
from . import views 

app_name = 'financial_products'
urlpatterns = [
    path('test/', views.api_test),
    # DB 저장
    path('deposit_save/', views.deposit_save),
    path('saving_save/' , views.saving_save),
    
    # DB에서 가져오기
    path('deposit_base_list/' , views.deposit_base_list),
    path('deposit_option_list/' , views.deposit_option_list),
    path('saving_base_list/' , views.saving_base_list),
    path('saving_option_list/' , views.saving_option_list),
    
   # 금융상품 포트폴리오 리스트 조회 및 생성 url
    path('port_folio/', views.portfolio_list),

    # 금융상품 포트폴리오
    path('port_folio/<int:product_id>/', views.portfolio_detail),
    path('algorithm/', views.recommend_product),
    path('deposit_options/<str:fin_prdt_cd>/', views.get_deposit_options),
]