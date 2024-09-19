from django.contrib import admin
from django.urls import path, include
from .views import BudgetCategoryListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('budget/', BudgetCategoryListCreateView.as_view(), name='budget-list-create'),  # 예산 설정 API
]
