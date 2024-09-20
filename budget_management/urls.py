from django.urls import path
from .views import BudgetCategoryListCreateView

urlpatterns = [
    path('budget/', BudgetCategoryListCreateView.as_view(), name='budget-list-create'),
]