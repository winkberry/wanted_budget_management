from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), #유저
    path('api/', include('budget_management.urls')), #예산
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 엑세스 토큰 갱신
    path('api/expenses/', include('expenses.urls')), #지출
]
