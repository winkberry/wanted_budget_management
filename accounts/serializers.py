from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호는 입력만 가능하고 출력은 제외

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])  # 비밀번호 암호화
        user.save()  # 저장
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # 인증 처리
        user = authenticate(username=data['username'], password=data['password'])

        if user and user.is_active:
            # JWT 토큰 발행
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")
    