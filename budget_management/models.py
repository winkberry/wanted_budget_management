from django.db import models
from django.conf import settings

class BudgetCategory(models.Model):
    CATEGORY_CHOICES = [
        ('food', '식비'),
        ('transport', '교통'),
        ('education', '교육'),
        ('beauty', '미용'),
        ('housing', '주거'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 유저와 연결
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # 카테고리 선택
    amount = models.PositiveIntegerField()  # 예산 금액 설정

    class Meta:
        unique_together = ('user', 'category')  # 유저별로 카테고리 중복 방지

    def __str__(self):
        return self.category  # 카테고리 코드를 반환
    
    
    