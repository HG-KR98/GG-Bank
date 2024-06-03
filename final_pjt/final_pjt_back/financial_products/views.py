from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
import requests
from rest_framework.response import Response
from .serializers import DepositProductListSerializers, SavingProducstsListSerializers, DepositOptionsListSerializers, SavingOptionsListSerializers, PortfolioListSerializer, PortfolioSerializer, DepositOptionSerializer
from rest_framework import status
from .models import DepositProducts, DepositOptions, SavingOptions, SavingProducts, Portfolio
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

from .utils import to_dict

# Create your views here.
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

# 정기예금 : 'S', 적금 : 'D', 연금저축 : 'P'
# 주택담보대출 : 'M', 전세자금대출 : 'R', 개인신용대출 : 'C'

# 은행 : '020000', 여신전문 : '030200', 저축은행 : '030300'
# 보험 : '050000', 금융투자 : '060000'

# 정기예금 depositProductsSearch.json 적금 savingProductsSearch.json
# 연금저축 annuitySavingProductsSearch.json 주택담보대출 mortgageLoanProductsSearch.json
# 전세자금대출 rentHouseLoanProductsSearch.json 개인신용대출 creditLoanProductsSearch.json

# 금융상품별 페이지 수
# 정기예금 : 은행 = 1, 여신전문 = 0, 저축은행 = 4, 보험 = 0, 금융투자 = 0
# 적금 : 은행 = 1, 여신전문 = 0, 저축은행 = 3, 보험 = 0, 금융투자 = 0 
# 연금저축 : 은행 = 0, 여신전문 = 0, 저축은행 = 0, 보험 = 10, 금융투자 = 60
# 주택담보대출 : 은행 = 1, 여신전문 = 0, 저축은행 = 1, 보험 = 1, 금융투자 = 0
# 전세자금대출 : 은행 = 1, 여신전문 = 0, 저축은행 = 1, 보험 = 1, 금융투자 = 0
# 개인신용대출 : 은행 = 1, 여신전문 = 1, 저축은행 = 1, 보험 = 1, 금융투자 = 0
companys = ['020000', '030200', '030300', '050000', '060000']

api_view(['GET'])
def api_test(request):
    URL = BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo' : 1
    }
    response = requests.get(URL, params=params).json()
    return JsonResponse({ 'response' : response })

# 데이터 저장 뷰 함수
# 정기 예금 baseList와 optionList 저장
@api_view(['GET'])
def deposit_save(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo' : 1,
    }
    response = requests.get(URL, params=params).json()
    BaseList = response.get('result').get('baseList')
    OptionList = response.get('result').get('optionList')

    for product in BaseList:
        fin_co_no = product.get('fin_co_no')
        dcls_month = product.get('dcls_month')
        fin_prdt_cd = product.get('fin_prdt_cd')
        kor_co_nm = product.get('kor_co_nm')
        fin_prdt_nm = product.get('fin_prdt_nm')
        join_way = product.get('join_way')
        mtrt_int = product.get('mtrt_int')
        spcl_cnd = product.get('spcl_cnd')
        join_deny = product.get('join_deny')
        join_member = product.get('join_member')
        etc_note = product.get('etc_note')
        max_limit = product.get('max_limit')
        dcls_strt_day = product.get('dcls_strt_day')
        dcls_end_day = product.get('dcls_end_day')
        fin_co_subm_day = product.get('fin_co_subm_day')
        
        if max_limit == None:
            max_limit = 0
        
        if dcls_end_day == None:
            dcls_end_day = '없음'

        if not DepositProducts.objects.filter(
            fin_prdt_cd = fin_prdt_cd
        ).exists():
            product_data = {
            'fin_co_no' : fin_co_no,
            'dcls_month' : dcls_month,
            'fin_prdt_cd' : fin_prdt_cd,
            'kor_co_nm' : kor_co_nm,
            'fin_prdt_nm' : fin_prdt_nm,
            'join_way' : join_way,
            'mtrt_int' : mtrt_int,
            'spcl_cnd' : spcl_cnd,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'etc_note' : etc_note,
            'max_limit' : max_limit,
            'dcls_strt_day' : dcls_strt_day,
            'dcls_end_day' : dcls_end_day,
            'fin_co_subm_day' : fin_co_subm_day,
        }
            serializer = DepositProductListSerializers(data=product_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
    for option in OptionList:
        dcls_month = option.get('dcls_month')
        fin_co_no = option.get('fin_co_no')
        fin_prdt_cd = option.get('fin_prdt_cd')
        intr_rate_type = option.get('intr_rate_type')
        intr_rate_type_nm = option.get('intr_rate_type_nm')
        save_trm = option.get('save_trm')
        intr_rate = option.get('intr_rate')
        intr_rate2 = option.get('intr_rate2')
        deposit_product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        if intr_rate == None:
            intr_rate = 0
        
        if intr_rate2 == None:
            intr_rate2 = 0

        option_data = {
            'dcls_month' : dcls_month,
            'fin_co_no' : fin_co_no,
            'fin_prdt_cd' : fin_prdt_cd,
            'intr_rate_type' : intr_rate_type,
            'intr_rate_type_nm' : intr_rate_type_nm,
            'save_trm' : save_trm,
            'intr_rate' : intr_rate,
            'intr_rate2' : intr_rate2,
        }    

        serializer = DepositOptionsListSerializers(data=option_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(deposit_product=deposit_product)
    return JsonResponse({'message' : '저장완료'})

# 적금 baseList와 optionList 저장
@api_view(['GET'])
def saving_save(request):
    URL = BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo' : 1,
    }
    response = requests.get(URL, params=params).json()
    BaseList = response.get('result').get('baseList')
    OptionList = response.get('result').get('optionList')

    for saving in BaseList:
        fin_co_no = saving.get('fin_co_no')
        dcls_month = saving.get('dcls_month')
        fin_prdt_cd = saving.get('fin_prdt_cd')
        kor_co_nm = saving.get('kor_co_nm')
        fin_prdt_nm = saving.get('fin_prdt_nm')
        join_way = saving.get('join_way')
        mtrt_int = saving.get('mtrt_int')
        spcl_cnd = saving.get('spcl_cnd') 
        join_deny = saving.get('join_deny')
        join_member = saving.get('join_member')
        etc_note = saving.get('etc_note')
        max_limit = saving.get('max_limit')
        dcls_strt_day = saving.get('dcls_strt_day')
        dcls_end_day = saving.get('dcls_end_day')
        fin_co_subm_day = saving.get('fin_co_subm_day')

        if max_limit == None:
            max_limit = 0
        
        if dcls_end_day == None:
            dcls_end_day = '없음'

        if not SavingProducts.objects.filter(
            fin_prdt_cd = fin_prdt_cd
        ).exists():
            product_data = {
            'fin_co_no' : fin_co_no,
            'dcls_month' : dcls_month,
            'fin_prdt_cd' : fin_prdt_cd,
            'kor_co_nm' : kor_co_nm,
            'fin_prdt_nm' : fin_prdt_nm,
            'join_way' : join_way,
            'mtrt_int' : mtrt_int,
            'spcl_cnd' : spcl_cnd,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'etc_note' : etc_note,
            'max_limit' : max_limit,
            'dcls_strt_day' : dcls_strt_day,
            'dcls_end_day' : dcls_end_day,
            'fin_co_subm_day' : fin_co_subm_day,
        }
            serializer = SavingProducstsListSerializers(data=product_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
    for option in OptionList:
        dcls_month = option.get('dcls_month')
        fin_co_no = option.get('fin_co_no')
        fin_prdt_cd = option.get('fin_prdt_cd')
        intr_rate_type = option.get('intr_rate_type')
        intr_rate_type_nm = option.get('intr_rate_type_nm')
        rsrv_type = option.get('rsrv_type')
        rsrv_type_nm = option.get('rsrv_type_nm')
        save_trm = option.get('save_trm')
        intr_rate = option.get('intr_rate')
        intr_rate2 = option.get('intr_rate2')
        saving_product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        if intr_rate == None:
            intr_rate = 0
        
        if intr_rate2 == None:
            intr_rate2 = 0

        option_data = {
                    'dcls_month' : dcls_month,
                    'fin_co_no' : fin_co_no,
                    'fin_prdt_cd' : fin_prdt_cd,
                    'intr_rate_type' : intr_rate_type,
                    'intr_rate_type_nm' : intr_rate_type_nm,
                    'rsrv_type' : rsrv_type,
                    'rsrv_type_nm' : rsrv_type_nm,
                    'save_trm' : save_trm,
                    'intr_rate' : intr_rate,
                    'intr_rate2' : intr_rate2,
                }    

        serializer = SavingOptionsListSerializers(data=option_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(saving_product=saving_product)    

    return JsonResponse({'message' : '저장완료'})


# 정기예금 base_list 보내기
@api_view(['GET'])
def deposit_base_list(request):
    deposits = list(map(to_dict, DepositProducts.objects.all()))
    options = list(map(to_dict, DepositOptions.objects.all()))
    data = []
    for deposit in deposits:
        # 6개월, 12개월, 24개월, 36개월 이자율
        trm = [0, 0, 0, 0]
        for option in options:
            if option.fin_prdt_cd == deposit.fin_prdt_cd:
                intr_1 = 0
                intr_2 = 0
                if option.save_trm == "6":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[0] = 0

                    else:    
                        trm[0] = round((intr_1 + intr_2) / 2, 2)

                
                if option.save_trm == "12":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[1] = 0

                    else:    
                        trm[1] = round((intr_1 + intr_2) / 2, 2)

                if option.save_trm == "24":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[2] = 0

                    else:    
                        trm[2] = round((intr_1 + intr_2) / 2, 2)

                if option.save_trm == "36":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[3] = 0

                    else:    
                        trm[3] = round((intr_1 + intr_2) / 2, 2)

        for i in range(4):
            if i == 0:
                setattr(deposit, "6", trm[0])
            elif i == 1:
                setattr(deposit, "12", trm[1])
            elif i == 2:
                setattr(deposit, "24", trm[2])
            else:
                setattr(deposit, "36", trm[3])

        data.append(deposit)
    
    return Response(data=data, status=status.HTTP_200_OK)
    # return JsonResponse(data=data, safe=False, json_dumps_params={'ensure_ascii': False}, )
    # return HttpResponse(json_data, status=status.HTTP_200_OK)

# deposit을 돌면서
# 2중 for문 options에서 deposit의 prdt_cd와 options의 prdt_cd가 같고 그 기간이 있으면 리스트에 
# 기간별로 [6개월, 12개월, 24개월, 36개월]에 조건문을 걸어서 넣는다.
# 

# 정기예금 option_list 보내기
@api_view(['GET'])
def deposit_option_list(request):
    options = DepositOptions.objects.all()
    serializer = DepositOptionsListSerializers(options, many=True)
    return Response(serializer.data)


# 적금 base_list 보내기
@api_view(['GET'])
def saving_base_list(request):
    savings = list(map(to_dict, SavingProducts.objects.all()))
    options = list(map(to_dict, SavingOptions.objects.all()))
    data = []
    for deposit in savings:
        trm = [0, 0, 0, 0]
        for option in options:
            if option.fin_prdt_cd == deposit.fin_prdt_cd:
                intr_1 = 0
                intr_2 = 0
                if option.save_trm == "6":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[0] = 0

                    else:    
                        trm[0] = round((intr_1 + intr_2) / 2, 2)

                
                if option.save_trm == "12":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[1] = 0

                    else:    
                        trm[1] = round((intr_1 + intr_2) / 2, 2)

                if option.save_trm == "24":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[2] = 0

                    else:    
                        trm[2] = round((intr_1 + intr_2) / 2, 2)

                if option.save_trm == "36":
                    if option.intr_rate != 0:
                        intr_1 = option.intr_rate

                    if option.intr_rate2 != 0:
                        intr_2 = option.intr_rate2 
                    
                    
                    if intr_1 == 0 and intr_2 == 0:
                        trm[3] = 0

                    else:    
                        trm[3] = round((intr_1 + intr_2) / 2, 2)
        
        for i in range(4):
            if i == 0:
                setattr(deposit, "6", trm[0])
            elif i == 1:
                setattr(deposit, "12", trm[1])
            elif i == 2:
                setattr(deposit, "24", trm[2])
            else:
                setattr(deposit, "36", trm[3])

        data.append(deposit)
    
    return Response(data=data, status=status.HTTP_200_OK)

# 적금 option_list 보내기
@api_view(['GET'])
def saving_option_list(request):
    options = SavingOptions.objects.all()
    serializer = SavingOptionsListSerializers(options, many=True)
    return Response(serializer.data)
    
# 금융상품 포트폴리오 생성 및 리스트 요청 함수
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST',])
def portfolio_list(request):
    if request.method == "GET":
        portfolios = Portfolio.objects.all()
        serializer = PortfolioListSerializer(portfolios, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# 금융상품 포트폴리오 삭제 함수
@permission_classes([IsAuthenticated])
@api_view(['DELETE',])
def portfolio_detail(request, product_id):
    portfolio = Portfolio.objects.get(pk=product_id)
    portfolio.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deposit_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionSerializer(options, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




## 금융 상품 추천

# 사용자 성향 점수화
def get_user_risk_score(gender, age, salary, asset):
    # 성별
    gender_score = 3 if gender == "남자" else 1

    # 나이
    if "20세 미만" in age or "20세 ~ 29세" in age:
        age_score = 3
    elif "30세 ~ 39세" in age or "40세 ~ 49세" in age:
        age_score = 2
    else:
        age_score = 1

    # 연봉
    if "1억원 이상" in salary or "8000만원 ~ 1억원" in salary:
        salary_score = 3
    elif "6000만원 ~ 8000만원" in salary or "4000만원 ~ 6000만원" in salary:
        salary_score = 2
    else:
        salary_score = 1

    # 자산
    if "2억원 ~ 4억원" in asset or "4억원 이상" in asset:
        asset_score = 3
    elif "1억원 ~ 2억원" in asset or "6000만원 ~ 1억원" in asset:
        asset_score = 2
    else:
        asset_score = 1

    # 토탈 점수 반환
    total_score = gender_score + age_score + salary_score + asset_score
    return total_score

def classify_user_risk(total_score):
    if 4 <= total_score <= 6:
        return "low"
    elif 7 <= total_score <= 9:
        return "medium"
    elif 10 <= total_score <= 12:
        return "high"
    else:
        return "unknown"

# 은행 규모에 따른 위험도 점수 정의
bank_risk_scores = {
    "국민은행": 1,
    "신한은행": 1,
    "하나은행": 1,
    "우리은행": 1,
    "농협은행주식회사": 1,
    "한국스탠다드차타드은행": 2,
    "중소기업은행": 2,
    "한국산업은행": 2,
    "주식회사 케이뱅크": 2,
    "주식회사 카카오뱅크": 2,
    "토스뱅크 주식회사": 2,
    "대구은행": 3,
    "부산은행": 3,
    "광주은행": 3,
    "제주은행": 3,
    "전북은행": 3,
    "경남은행": 3,
    "수협은행": 3
}

# 금리 점수 정의
def get_interest_score(interest_rate):
    if 1.27 <= interest_rate <= 2.59:
        return 1
    elif 2.6 <= interest_rate <= 3.9:
        return 2
    elif 4.0 <= interest_rate <= 5.2:
        return 3
    else:
        return 0

# 기간 점수 정의
def get_duration_score(duration):
    if duration <= 6:
        return 1
    elif duration <= 12:
        return 2
    elif duration <= 24:
        return 3
    else:
        return 4

# 예금 및 적금 상품 점수화 및 추천 로직
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_product(request):
    # 사용자 정보 가져오기
    gender = request.GET.get('gender')
    age = request.GET.get('age')
    salary = request.GET.get('salary')
    asset = request.GET.get('asset')

    # 사용자 성향 점수 계산
    user_risk_score = get_user_risk_score(gender, age, salary, asset)
    user_risk_class = classify_user_risk(user_risk_score)
    
    # 추천 상품 가져오기 함수
    def get_recommended_products(product_model, option_model, product_type):
        recommended_products = []

        # 모든 상품 가져오기
        products = product_model.objects.all()

        for product in products:
            # 상품 옵션 가져오기
            options = option_model.objects.filter(deposit_product=product) if product_type == "예금" else option_model.objects.filter(saving_product=product)
            for option in options:
                # 평균 이자율 계산
                avg_interest_rate = (option.intr_rate + option.intr_rate2) / 2 if option.intr_rate and option.intr_rate2 else option.intr_rate
                # 은행 점수, 이자율 점수, 기간 점수 계산
                bank_score = bank_risk_scores.get(product.kor_co_nm, 3)
                interest_score = get_interest_score(avg_interest_rate)
                duration_score = get_duration_score(int(option.save_trm))

                # 총 점수 계산
                total_score = bank_score + interest_score + duration_score

                # 상품 위험도 분류
                if 3 <= total_score <= 5:
                    product_risk_class = "low"
                elif 6 <= total_score <= 7:
                    product_risk_class = "medium"
                elif 8 <= total_score <= 10:
                    product_risk_class = "high"
                else:
                    product_risk_class = "unknown"

                # 사용자와 일치하는 위험도인 상품만 추가
                if product_risk_class == user_risk_class:
                    recommended_products.append({
                        "product_type": product_type,
                        "product": product,
                        "options": option,
                        "total_score": total_score
                    })

        return recommended_products

    # 예금 및 적금 추천 상품 가져오기
    recommended_deposit_products = get_recommended_products(DepositProducts, DepositOptions, "예금")
    recommended_saving_products = get_recommended_products(SavingProducts, SavingOptions, "적금")
    
    # 모든 추천 상품(예금 + 적금) 합치기 및 점수로 정렬
    all_recommended_products = recommended_deposit_products + recommended_saving_products
    all_recommended_products = sorted(all_recommended_products, key=lambda x: x['total_score'])

    # 중복 제거 및 점수(위험도) 낮은 순으로 정렬
    unique_products = {}
    for item in all_recommended_products:
        product_name = item["product"].fin_prdt_nm
        if product_name not in unique_products:
            unique_products[product_name] = item
        else:
            if item['total_score'] < unique_products[product_name]['total_score']:
                unique_products[product_name] = item

    sorted_unique_products = sorted(unique_products.values(), key=lambda x: x['total_score'])

    # 결과 데이터 생성
    response_data = []
    for item in sorted_unique_products:
        product = item["product"]
        option = item["options"]
        # 단기는 24, 36 금리가 필요없음
        if request.GET.get('tendency') == '단기':
            if option.save_trm == "6" or option.save_trm == "12":
                response_data.append({
                    "product_type": item["product_type"],
                    "dcls_month": product.dcls_month,
                    "kor_co_nm": product.kor_co_nm,
                    "fin_prdt_nm": product.fin_prdt_nm,
                    "six_month": option.intr_rate if option.save_trm == "6" else None,
                    "twelve_month": option.intr_rate if option.save_trm == "12" else None,
                    "twenty_four_month": None,
                    "thirty_six_month": None,
                })
        elif request.GET.get('tendency') == '중기':
            if option.save_trm == "12" or option.save_trm == "24":
                response_data.append({
                    "product_type": item["product_type"],
                    "dcls_month": product.dcls_month,
                    "kor_co_nm": product.kor_co_nm,
                    "fin_prdt_nm": product.fin_prdt_nm,
                    "six_month": None,
                    "twelve_month": option.intr_rate if option.save_trm == "12" else None,
                    "twenty_four_month": option.intr_rate if option.save_trm == "24" else None,
                    "thirty_six_month": None,
                })
        elif request.GET.get('tendency') == '장기':
            if option.save_trm == "24" or option.save_trm == "36":
                response_data.append({
                    "product_type": item["product_type"],
                    "dcls_month": product.dcls_month,
                    "kor_co_nm": product.kor_co_nm,
                    "fin_prdt_nm": product.fin_prdt_nm,
                    "six_month": None,
                    "twelve_month": None,
                    "twenty_four_month": option.intr_rate if option.save_trm == "24" else None,
                    "thirty_six_month": option.intr_rate if option.save_trm == "36" else None,
                })

    # 응답 반환
    return Response(response_data, status=status.HTTP_200_OK)
