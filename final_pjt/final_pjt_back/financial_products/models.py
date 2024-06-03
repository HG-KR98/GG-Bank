from django.db import models
from django.conf import settings
# 정기 예금 데이터 모델
# 만기 후 이자율과 기타 유의 사항은 따로 버튼을 만들어서 창을 띄우기
class DepositProducts(models.Model):
    fin_co_no = models.TextField() # 금융회사 번호
    # datefield로는 저장이 가능한지...
    dcls_month = models.TextField() # 공시월
    fin_prdt_cd = models.TextField(unique=True) # 금융상품코드
    kor_co_nm = models.TextField() # 금융회사명
    fin_prdt_nm = models.TextField() # 금융상품명 
    join_way = models.TextField() # 가입방법
    mtrt_int = models.TextField() # 만기후 이자율
    spcl_cnd = models.TextField() # 특별조건
    join_deny = models.TextField() # 가입제한
    join_member = models.TextField() # 가입대상
    etc_note = models.TextField() # 기타유의사항
    max_limit = models.FloatField(null=True) # 최고한도
    # "YYYY-MM-DD"의 형식으로 받아져야 DateField형식으로 저장이 되므로 
    # 이와 관련된 처리가 필요하다.
    dcls_strt_day = models.TextField() # 공시시작일
    dcls_end_day = models.TextField(null=True) # 공시종료일
    fin_co_subm_day = models.TextField() # 금융회사제출일

class DepositOptions(models.Model):
    deposit_product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options') # 외래키
    dcls_month = models.TextField() # 공시월
    fin_co_no = models.TextField() # 금융회사번호
    fin_prdt_cd = models.TextField() # 금융상품코드
    intr_rate_type = models.TextField() # 이자율유형
    intr_rate_type_nm = models.TextField() # 이자율유형명
    # 저축 기간을 integer로 저장할지 고민이 된다.
    save_trm = models.TextField() # 저축 기간
    intr_rate = models.FloatField(null=True) # 이자율
    intr_rate2 = models.FloatField(null=True) # 우대 이자율

# 적금 데이터 모델
class SavingProducts(models.Model):
    # integer로 저장할지 고민 중
    fin_co_no = models.TextField()
    # datetime
    dcls_month = models.TextField()
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    kor_co_nm = models.TextField()  # 금융회사명(한글)
    fin_prdt_nm = models.TextField()  # 금융상품명
    join_way = models.TextField()  # 가입방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    # 없음이라는 데이터가 존재함 전처리에서 주의하기 !!
    spcl_cnd = models.TextField()  # 특별조건
    join_deny = models.TextField()  # 가입제한
    # 제한 없음이라는 데이터가 존재함
    join_member = models.TextField() # 가입대상
    etc_note = models.TextField()  # 기타유의사항
    max_limit = models.FloatField(null=True)  # 최고한도액
    # datefield
    dcls_strt_day = models.TextField()  # 공시시작일
    dcls_end_day = models.TextField(null=True) # 공시종료일
    # datetimefield
    fin_co_subm_day = models.TextField()  # 금융회사 제출일


class SavingOptions(models.Model):
    saving_product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    dcls_month = models.TextField()  # 공시월
    fin_co_no = models.TextField()  # 금융회사 번호
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type = models.TextField()  # 이율유형
    intr_rate_type_nm = models.TextField()  # 이율유형명
    rsrv_type = models.TextField()  # 적립유형
    rsrv_type_nm = models.TextField()  # 적립유형명
    save_trm = models.TextField() # 적립기간
    intr_rate = models.FloatField(null=True)  # 이율
    intr_rate2 = models.FloatField(null=True)  # 이율2

# 금융 상품 포트폴리오
class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_kind = models.TextField() # 금융상품 종류 (정기예금, 정기적금)
    fin_prdt_nm = models.TextField() # 금융상품 이름
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    kor_co_nm = models.TextField() # 금융회사명
    tweleve_month = models.FloatField() # 12개월 이율
