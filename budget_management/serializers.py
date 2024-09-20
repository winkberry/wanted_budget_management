from rest_framework import serializers
from .models import BudgetCategory

class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = ['category', 'amount']  # 카테고리와 예산 금액만 입력받음

    def create(self, validated_data):
        user = self.context['request'].user  # 현재 요청한 유저 가져오기
        category = validated_data.get('category')
        amount = validated_data.get('amount')
        budget, created = BudgetCategory.objects.update_or_create(
            user=user,
            category=category,
            defaults={'amount': amount}
        )
        return budget