from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('budget_management.urls')), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 리프레시 토큰 URL 추가
]
