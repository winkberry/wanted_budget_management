from django.contrib import admin
from .models import Expense

# Expense 모델을 Admin에 등록
admin.site.register(Expense)