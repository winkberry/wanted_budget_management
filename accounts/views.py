from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError



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
    
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token is None:
                raise ValidationError("Refresh token is required.")

            token = RefreshToken(refresh_token)
            token.blacklist()  # 리프레시 토큰을 블랙리스트에 추가
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error during logout: {e}")  # 디버깅 메시지 출력
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
