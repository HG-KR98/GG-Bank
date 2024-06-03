from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer, TokenSerializer, UserDetailsSerializer, TokenModel
from dj_rest_auth.registration.serializers import RegisterSerializer


User = get_user_model()

# 회원가입 커스텀
class CustomRegisterSerializer(RegisterSerializer):
    # 커스텀할 항목들
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    birth_date = serializers.DateField()
    name = serializers.CharField()
    assets = serializers.IntegerField()

    # 추가한 항목의 데이터를 저장하는 메서드
    def save(self, request):
        user = super().save(request)
        user.phone_number = self.data.get('phone_number')
        user.birth_date = self.data.get('birth_date')
        user.gender = self.data.get('gender')
        user.name = self.data.get('name')
        user.assets = self.data.get('assets')
        user.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

class CustomTokenSerializer(TokenSerializer):
    user = CustomUserDetailsSerializer()

    class Meta:
        model = TokenModel
        fields = ('key', 'user')

class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(allow_blank=True)
    email = None
    
    
# 회원정보수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'name', 'gender', 'birth_date', 'assets', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.assets = validated_data.get('assets', instance.assets)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance