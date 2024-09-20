from django.urls import path
from .views import BudgetCategoryBulkCreateView

urlpatterns = [
    path('budget/', BudgetCategoryBulkCreateView.as_view(), name='budget-bulk-create'),
]