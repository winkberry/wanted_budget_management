from django.db import models
from django.contrib.auth import get_user_model
from budget_management.models import BudgetCategory  # 예산 카테고리 모델 가져오기

User = get_user_model()

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 지출을 생성한 유저
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)  # 지출 카테고리
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 지출 금액
    date = models.DateField()  # 지출 일자
    memo = models.TextField(null=True, blank=True)  # 지출 메모
    excluded_from_total = models.BooleanField(default=False)  # 합계제외 여부

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"