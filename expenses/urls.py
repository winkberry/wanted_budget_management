from django.urls import path
from .views import ExpenseCreateView, ExpenseListView, ExpenseUpdateView, DailyExpenseSummaryView, DailyBudgetRecommendationView

urlpatterns = [
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('list/', ExpenseListView.as_view(), name='expense-list'),
    path('update/<int:pk>/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('daily-summary/', DailyExpenseSummaryView.as_view(), name='daily-summary'),
    path('daily-recommendation/', DailyBudgetRecommendationView.as_view(), name='daily-recommendation'),
]