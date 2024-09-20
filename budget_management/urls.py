from django.urls import path
from .views import BudgetCategoryBulkCreateView, CategoryListView, BudgetRecommendationView

urlpatterns = [
    path('budget/', BudgetCategoryBulkCreateView.as_view(), name='budget-bulk-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),  # 카테고리 목록 API
    path('budget/recommendation/', BudgetRecommendationView.as_view(), name='budget-recommendation'), #예산 추천
]