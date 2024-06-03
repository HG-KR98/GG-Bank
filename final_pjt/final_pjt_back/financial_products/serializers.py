from rest_framework import serializers
from .models import DepositProducts, SavingProducts, DepositOptions, SavingOptions, Portfolio


# 정기 예금 옵션 serializer
class DepositOptionsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = "__all__"
        read_only_fields = ('deposit_product',)

# 정기 예금 베이스 serializer
class DepositProductListSerializers(serializers.ModelSerializer):

    class Meta:
        model = DepositProducts
        fields = "__all__"



# 적금 옵션 serializer
class SavingOptionsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('saving_product',)

# 적금 베이스 serializer
class SavingProducstsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = "__all__"


# 금융상품 포트폴리오 리스트
class PortfolioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"

# 금융상품 포트폴리오 상세정보 및 삭제 그리고 추가
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"
        read_only_fields = ('user',)
        
from rest_framework import serializers

    
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'