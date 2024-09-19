from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# 현재 설정된 CustomUser 모델 가져오기
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 인증 없이 접근 가능하게 설정

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # 인증 없이 접근 가능하게 설정

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
    