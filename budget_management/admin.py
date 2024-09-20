from django.contrib import admin
from .models import BudgetCategory

# BudgetCategory 모델을 Admin에 등록
admin.site.register(BudgetCategory)